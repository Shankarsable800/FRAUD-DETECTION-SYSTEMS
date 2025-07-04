from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import  UserDetails, Users
from detection.models import Transaction
from django.db.models import Sum

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print("user: ", user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        try:
            username = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('name')
            user_object = Users.objects.create_user(first_name=first_name, username=username, password=password)
            user_object.save()
            return render(request, 'login.html')
        except Exception as e:
            return render(request, 'register.html', {'error_message': 'Username already exists'})


class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        # Fetch user details from the database
        try:
            fraud_count = Transaction.objects.filter(user=request.user, is_fraud=True).count()
            transaction_count = Transaction.objects.filter(user=request.user).count()
            total_credit = Transaction.objects.filter(user=request.user).aggregate(Sum('credit'))['credit__sum'] or 0
            total_lost_funds = Transaction.objects.filter(user=request.user, is_fraud=True).aggregate(Sum('debit'))['debit__sum'] or 0
            total_debit = Transaction.objects.filter(user=request.user).aggregate(Sum('debit'))['debit__sum'] or 0
            total_funds = total_credit - total_debit
        except UserDetails.DoesNotExist:
            user_details = None

        return render(request, 'index.html', {'name': request.user.username, 
                                              'fraud_count': fraud_count,
                                              'transaction_count':transaction_count,
                                              'total_funds': total_funds,
                                              'total_lost_funds': total_lost_funds,
                                              })
    
    def post(self, request):
        print(request.user)
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'index.html')

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')
    



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .ml_utils import predict_fraud
from .models import Users
from detection.models import Transaction
from .serializers import TransactionSerializer
import uuid

@api_view(['POST'])
def predict_transaction(request):
    required_fields = ['recipient', 'amount', 'description']
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"Missing required field: {field}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    data = request.data.copy()
    data["transaction_id"] = str(uuid.uuid4())

    fraud_score, is_fraud = predict_fraud(data)
    data["fraud_score"] = round(fraud_score, 4)
    data["is_fraud"] = is_fraud

    serializer = TransactionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
# Send email alert to user if fraud is detected
        if is_fraud and request.user.is_authenticated:
            from django.core.mail import send_mail
            subject = "🚨 Fraud Alert: Suspicious Transaction Detected"
            message = f"""
Dear {request.user.first_name},

A transaction of ₹{data['amount']} to recipient '{data['recipient']}' was flagged as fraudulent.
Please review your account immediately.

Regards,
FraudDetection Team
"""
            send_mail(subject, message, None, [request.user.email], fail_silently=True)
        return Response({
            "message": "Transaction processed.",
            "fraud_score": round(fraud_score, 4),
            "is_fraud": is_fraud,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
