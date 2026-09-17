from users_app.models import UserProfile


def profiles_by_type(profile_type):
    """Return profiles matching a supported profile type."""
    return UserProfile.objects.filter(type=profile_type)