from django.urls import path
from . import views
from . import reminder_views
from . import migration_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:reservation_id>/update/', views.reservation_update, name='reservation_update'),
    path('reservations/<int:reservation_id>/cancel/', views.reservation_cancel, name='reservation_cancel'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('reminders/', reminder_views.reminder_list, name='reminder_list'),
    path('force-migrate/', migration_views.force_migrate, name='force_migrate'),
    path('manager/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/rooms/', views.admin_room_manage, name='admin_room_manage'),
    path('manager/reservations/', views.admin_reservation_manage, name='admin_reservation_manage'),
    path('manager/reservations/create/', views.admin_reservation_create, name='admin_reservation_create'),
    path('manager/reservations/<int:reservation_id>/cancel/', views.admin_reservation_cancel, name='admin_reservation_cancel'),
    path('manager/reminders/', reminder_views.admin_reminder_manage, name='admin_reminder_manage'),
    path('api/rooms/<int:room_id>/availability/', views.check_room_availability, name='check_room_availability'),
]