from users_app.models import UserProfile


def business_profiles():
    """Return profiles belonging to business users."""
    return UserProfile.objects.filter(type='business')