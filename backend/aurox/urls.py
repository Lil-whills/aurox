from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('bookmarks/save/<int:property_id>/', views.save_bookmark, name='save_bookmark'),
    path('bookmarks/delete/<int:property_id>/', views.delete_bookmark, name='delete_bookmark'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('about/', views.about, name='about'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('properties/', views.properties, name='properties'),
    path('propertydetail/<int:property_id>/', views.propertydetail, name='propertydetail'),
]