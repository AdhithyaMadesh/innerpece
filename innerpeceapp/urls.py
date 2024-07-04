from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('admin_user_crud/', views.admin_user_crud, name='admin_user_crud'),
    path('create_user/', views.create_user, name='create_user'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('logout/',views.user_logout, name="logout"),
    path('create/', views.create_tour, name='create_tour'),
    path('tour_list/',views.tour_list, name="tour_list"),
    path('update/<int:pk>/', views.update_tour, name='update_tour'),
    path('delete/<int:pk>/', views.delete_tour, name='delete_tour'),
    path('user_tour_list/',views.user_tour_list, name="user_tour_list"),
    path('user_tour_full_view/<int:pk>/',views.user_tour_full_view, name='user_tour_full_view'),
]
