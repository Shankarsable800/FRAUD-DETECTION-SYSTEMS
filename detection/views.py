from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.views import View 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import re
import json
import datetime
from datetime import timedelta

from .models import FraudData, Transaction, FraudAccount


# -------------------------------
# AddFraud View
# -------------------------------
@login_required
class AddFraud(View):
    def get(self, request):
        fraud_list = FraudData.objects.filter(user=request.user)
        return render(request, 'add-fraud.html', {'fraud_list': fraud_list, 'name': request.user.username})

    def post(self, request):
        fraud_type = request.POST.get('fraud_type')
        fraud_data = request.POST.get('fraud')
        
        if fraud_type:
            if fraud_type == '1':
                fraud_type = 'Mobile Number'
            elif fraud_type == '2':
                fraud_type = 'Account Number'
            
            FraudData.objects.create(
                user=request.user,
                fraud_type=fraud_type,
                fraud_description=fraud_data
            )
        else:
            fraud_list = FraudData.objects.filter(user=request.user)
            return render(request, 'add-fraud.html', {
                'fraud_list': fraud_list,
                'error_message': 'No fraud data provided.',
                'name': request.user.username
            })

        fraud_list = FraudData.objects.filter(user=request.user)
        return render(request, 'add-fraud.html', {'fraud_list': fraud_list, 'name': request.user.username})


# -------------------------------
# Dashboard View
# -------------------------------
@login_required
def dashboard_view(request):
    user = request.user
    fraud_count = Transaction.objects.filter(user=user, is_fraud=True).count()
    transaction_count = Transaction.objects.filter(user=user).count()
    total_credits = Transaction.objects.filter(user=user).aggregate(Sum('credit'))['credit__sum'] or 0
    total_debits = Transaction.objects.filter(user=user).aggregate(Sum('debit'))['debit__sum'] or 0
    total_funds = total_credits - total_debits
    total_lost_funds = Transaction.objects.filter(user=user, is_fraud=True, debit__gt=0).aggregate(Sum('debit'))['debit__sum'] or 0

    return render(request, 'index.html', {
        'name': user.username,
        'fraud_count': fraud_count,
        'transaction_count': transaction_count,
        'total_funds': total_funds,
        'total_lost_funds': total_lost_funds,
    })


# -------------------------------
# Fraud Dashboard (Chart View)
# -------------------------------
@login_required
def fraud_dashboard_view(request):
    user = request.user
    fraud_count = Transaction.objects.filter(user=user, is_fraud=True).count()
    non_fraud_count = Transaction.objects.filter(user=user, is_fraud=False).count()
    
    monthly_fraud_data = (
        Transaction.objects.filter(user=user, is_fraud=True)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = [item['month'].strftime("%b %Y") for item in monthly_fraud_data]
    counts = [item['count'] for item in monthly_fraud_data]

    return render(request, 'fraud_dashboard.html', {
        'name': user.username,
        'fraud_count': fraud_count,
        'non_fraud_count': non_fraud_count,
        'months': months,
        'counts': counts
    })


# -------------------------------
# Fraud Transactions View
# -------------------------------
@login_required
def fraud_transactions_view(request):
    user = request.user
    all_transactions = Transaction.objects.filter(user=user, is_fraud=True).order_by('-date')

    paginator = Paginator(all_transactions, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'fraud_transactions.html', {
        'transactions': page_obj,
        'name': user.username,
    })


# -------------------------------
# All Transactions View
# -------------------------------
@login_required
def all_transactions_view(request):
    user = request.user
    all_transactions = Transaction.objects.filter(user=user).order_by('-date')

    paginator = Paginator(all_transactions, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_transactions.html', {
        'transactions': page_obj,
        'name': user.username,
    })


# -------------------------------
# Total Funds View
# -------------------------------
@login_required
@login_required
def Total_Funds_view(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')

    debit_txns = transactions.filter(debit__isnull=False)
    credit_txns = transactions.filter(credit__isnull=False)

    total_debit = debit_txns.aggregate(Sum('debit'))['debit__sum'] or 0
    total_credit = credit_txns.aggregate(Sum('credit'))['credit__sum'] or 0

    # Safely assign recipient for display (does not overwrite model field)
    for tx in debit_txns:
        if tx.description:
            match = re.search(r'/DR/([^/]+)', tx.description)
            tx.recipient_display = match.group(1).strip() if match else 'unknown'
        else:
            tx.recipient_display = 'unknown'

    # Ensure credit transactions have a display-friendly description
    for tx in credit_txns:
        if not tx.description:
            tx.description = 'No description'

    return render(request, 'Total_Funds.html', {
        'name': user.username,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'debit_transactions': debit_txns,
        'credit_transactions': credit_txns,
    })

# -------------------------------
# Lost Funds View
# -------------------------------
@login_required
def lost_funds_transactions_view(request):
    user = request.user
    lost_transactions = Transaction.objects.filter(user=user, is_fraud=True).order_by('-date')

    paginator = Paginator(lost_transactions, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lost_transactions.html', {
        'transactions': page_obj,
        'name': user.username,
    })


# -------------------------------
# Add Transaction View (manual)
# -------------------------------
@login_required
def add_transaction_view(request):
    user = request.user
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        amount = float(request.POST.get('amount'))
        txn_type = request.POST.get('type')
        description = request.POST.get('description')

        is_fraud = False
        now_time = timezone.now()

        # Rule 1: Midnight txn
        if 0 <= now_time.hour < 4:
            is_fraud = True

        # Rule 2: Multiple high txns to same recipient in 1 hr
        if Transaction.objects.filter(user=user, recipient=recipient, debit__gte=50000, date__gte=now_time - timedelta(hours=1)).count() >= 2:
            is_fraud = True

        # Rule 3: Too many txns in 30 min
        if Transaction.objects.filter(user=user, date__gte=now_time - timedelta(minutes=30)).count() > 10:
            is_fraud = True

        # Rule 4: Sudden spike in amount
        last_txns = Transaction.objects.filter(user=user).order_by('-date')[:5]
        avg_amount = sum(t.amount for t in last_txns if t.amount) / max(len(last_txns), 1)
        if avg_amount > 0 and amount > 5 * avg_amount:
            is_fraud = True

        Transaction.objects.create(
            user=user,
            recipient=recipient,
            description=description,
            amount=amount,
            debit=amount if txn_type == 'debit' else None,
            credit=amount if txn_type == 'credit' else None,
            is_fraud=is_fraud,
        )

        return JsonResponse({'status': 'fraud' if is_fraud else 'safe'})


# -------------------------------
# Receive Transaction API (auto insert)
# -------------------------------
@csrf_exempt
def receive_transaction_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')

        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'status': 'error', 'message': 'Invalid user'}, status=400)

        recipient = str(data.get('recipient', '')).strip()
        amount = float(data.get('amount', 0))
        description = data.get('description', '')
        sender_phone = str(data.get('sender_phone', '')).replace(" ", "").strip()
        now_time = timezone.now()
        is_fraud = False

        # Rule 1: Midnight txn
        if 0 <= now_time.hour < 4:
            is_fraud = True

        # Rule 2: High txns to same recipient
        if Transaction.objects.filter(user=user, recipient=recipient, debit__gte=50000, date__gte=now_time - timedelta(hours=1)).count() >= 2:
            is_fraud = True

        # Rule 3: Too frequent txns
        if Transaction.objects.filter(user=user, date__gte=now_time - timedelta(minutes=30)).count() > 10:
            is_fraud = True

        # Rule 4: Amount spike
        last_txns = Transaction.objects.filter(user=user).order_by('-date')[:5]
        avg_amount = sum(t.amount for t in last_txns if t.amount) / max(len(last_txns), 1)
        if avg_amount > 0 and amount > 5 * avg_amount:
            is_fraud = True

        # Rule 5: In blacklist or fraud list
        if FraudAccount.objects.filter(account_number=recipient).exists():
            is_fraud = True
        for entry in FraudData.objects.filter(user=user):
            if (entry.fraud_type == 'Account Number' and recipient == entry.fraud_description.strip()) or \
               (entry.fraud_type == 'Mobile Number' and sender_phone == entry.fraud_description.strip()):
                is_fraud = True
                break

        Transaction.objects.create(
            user=user,
            recipient=recipient,
            amount=amount,
            description=description,
            debit=amount,
            is_fraud=is_fraud,
        )

        return JsonResponse({'status': 'fraud' if is_fraud else 'safe'})
