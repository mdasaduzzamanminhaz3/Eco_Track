from django.contrib import admin
from .models import UserWallet, TransactionHistory
# Register your models here.
admin.site.register(UserWallet)
admin.site.register(TransactionHistory)