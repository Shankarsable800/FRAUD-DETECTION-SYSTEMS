from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    """
    Custom user model extending AbstractUser.
    """
    # Add any additional fields you want to include in your user model
    # For example:
    # bio = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']
        db_table = 'users'


class UserDetails(models.Model):
    """
    Model to store additional user details.
    """
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    # Add any additional fields you want to include in your user details
    # For example:
    # bio = models.TextField(blank=True, null=True)
    total_frauds = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
    total_funds = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    total_lost_funds = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    
    def __str__(self):
        return f"{self.user.first_name} - Details"
