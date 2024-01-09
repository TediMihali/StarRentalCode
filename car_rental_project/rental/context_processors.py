from .models import Customer

def staff_account(request):
    staff_account_value = False  # Default value

    if request.user.is_authenticated:
        try:
            customer_instance = Customer.objects.get(user=request.user)
            staff_account_value = customer_instance.staff_account
        except Customer.DoesNotExist:
            pass

    return {'staff_account': staff_account_value}
