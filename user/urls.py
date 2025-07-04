from django.urls import path
from .views import (
    LoginView, HomeView, LogoutView, RegisterView,
    predict_transaction # 👈 add this
)

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('home', HomeView.as_view(), name='home'),
    path('register', RegisterView.as_view(), name='register'),
    #path('add-fraud/', AddFraudView.as_view(), name='add_fraud'),

    # ✅ New API route for fraud prediction
    path('api/predict/', predict_transaction, name='predict_transaction'),
]

