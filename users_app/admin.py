from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	extra = 0


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	inlines = [UserProfileInline]
	list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
	search_fields = ('username', 'email')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'type', 'location', 'tel', 'uploaded_at')
	list_filter = ('type', 'uploaded_at')
	search_fields = ('user__username', 'user__email', 'location')
