from django.contrib import admin
from .models import Wallet, Transaction, Withdrawal
from .services import process_withdrawal

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Transaction)

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'status', 'created_at']

    def save_model(self, request, obj, form, change):
        # Check previous status
        if change:
            old_obj = Withdrawal.objects.get(pk=obj.pk)

        super().save_model(request, obj, form, change)  # save first

        if old_obj.status != 'approved' and obj.status == 'approved':
            result = process_withdrawal(obj)

            if result.get("error"):
                obj.status = 'rejected'
                obj.save()
        else:
            super().save_model(request, obj, form, change)