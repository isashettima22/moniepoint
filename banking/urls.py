from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('transfer/', views.transfer, name='transfer'),
    path('transfer/review/', views.transfer_review, name='transfer_review'),
    path('transfer/confirm/', views.confirm_transfer, name='confirm_transfer'),

    path('transactions/', views.transaction_history, name='transaction_history'),

    path('airtime/', views.airtime, name='airtime'),
    path('airtime/review/', views.airtime_review, name='airtime_review'),
    path('airtime/confirm/', views.confirm_airtime, name='confirm_airtime'),

    path('data-bundle/', views.data_bundle, name='data_bundle'),
    path('data-review/', views.data_review, name='data_review'),
    path('data-confirm/', views.confirm_data, name='confirm_data'),

    path('electricity/', views.electricity, name='electricity'),
    path('electricity/review/', views.electricity_review, name='electricity_review'),
    path('electricity/confirm/', views.confirm_electricity, name='confirm_electricity'),

    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),

    # TV Subscription URLs
    path('tv-subscription/', views.tv_subscription, name='tv_subscription'),
    path('tv-review/', views.tv_review, name='tv_review'),
    path('tv-confirm/', views.confirm_tv, name='confirm_tv'),

    # Water Bill URLs
    path('water-bill/', views.water_bill, name='water_bill'),
    path('water-review/', views.water_review, name='water_review'),
    path('water-confirm/', views.confirm_water, name='confirm_water'),

    path(
        'transaction-receipt/<int:transaction_id>/',
        views.transaction_receipt,
        name='transaction_receipt'
    ),
]