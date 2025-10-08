from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Room, Reservation, Notification, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_is_admin')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    def get_is_admin(self, obj):
        return obj.profile.is_admin if hasattr(obj, 'profile') else False
    get_is_admin.short_description = 'Is Admin'
    get_is_admin.boolean = True


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'location', 'description')
    list_editable = ('is_active',)
    ordering = ('name',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'user', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'room', 'start_time', 'created_at')
    search_fields = ('title', 'user__username', 'room__name')
    list_editable = ('status',)
    ordering = ('-start_time',)
    date_hierarchy = 'start_time'
    
    fieldsets = (
        ('Reservation Details', {
            'fields': ('title', 'description', 'room', 'user')
        }),
        ('Time Details', {
            'fields': ('start_time', 'end_time')
        }),
        ('Status', {
            'fields': ('status', 'created_by_admin')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('room', 'user')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    list_editable = ('is_read',)
    ordering = ('-created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'department', 'is_admin')
    list_filter = ('is_admin', 'department')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_editable = ('is_admin',)


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)