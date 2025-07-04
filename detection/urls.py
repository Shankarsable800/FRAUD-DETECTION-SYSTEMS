from django.urls import path
#from .views import AddFraud, UploadStatement

#from .views import fraud_transactions_view
#from .views import lost_funds_transactions_view
#from .views import all_transactions_view
from detection.views import*


    # your existing routes

urlpatterns = [
    path('add-fraud/', AddFraud, name='add_fraud'),
    path('fraud-transactions/', fraud_transactions_view, name='fraud-transactions'),
    path('lost-transactions/', lost_funds_transactions_view, name='lost-transactions'),
    path('all-transactions/', all_transactions_view, name='all-transactions'),
    path('total-funds/', Total_Funds_view, name='total-funds'),
    path('', dashboard_view, name='dashboard'),
    path('fraud-dashboard/', fraud_dashboard_view, name='fraud_dashboard'),
    path('add-transaction/', add_transaction_view, name='add_transaction'),
    path('api/receive-txn/', receive_transaction_api, name='receive_transaction_api'), #FOR THIS api attachecd for automatically data inserting
]


   
