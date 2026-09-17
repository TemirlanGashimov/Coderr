from django.db.models import Q

from orders_app.models import Order


def orders_for_user(user):
    """Return orders visible to a customer or business user."""
    return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))


def orders_for_business_user(user, status):
    """Return a business user's orders with the requested status."""
    return Order.objects.filter(business_user=user, status=status)