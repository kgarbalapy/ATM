from django.contrib import admin
from .models import BankAccount, TransactionHistory


class BankAccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BankAccount._meta.fields if field.name != "id"]


class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TransactionHistory._meta.fields if field.name != "id"]


admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
