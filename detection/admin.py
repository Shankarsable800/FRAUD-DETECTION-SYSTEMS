from django.contrib import admin
from .models import Transaction, FraudAccount

# Register the models so they show up in the admin panel
admin.site.register(Transaction)
admin.site.register(FraudAccount)
