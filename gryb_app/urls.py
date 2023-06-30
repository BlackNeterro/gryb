from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'gryb_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('contact/', views.contact, name='contact'),
    path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('contact_thank_you/', views.contact_thank_you, name='contact_thank_you'),
    path('login/', auth_views.LoginView.as_view(template_name='gryb_app/login.html'), name='login'),
    path('registration/', views.registration, name='registration'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
     path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='gryb_app/password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('abaut/', views.abaut, name='abaut')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

