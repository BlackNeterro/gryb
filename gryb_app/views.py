from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Comment, Cart, Product, CarouselImage
from .forms import CommentForm, CartForm, ContactForm, RegistrationForm, EditProfileForm, ChangePasswordForm, OrderForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from .models import Video
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('gryb_app:login')
    else:
        form = RegistrationForm()
    return render(request, 'gryb_app/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('gryb_app:cart')
    else:
        form = AuthenticationForm()
    return render(request, 'gryb_app/login.html', {'form': form})


def home(request):
    products = Product.objects.all()
    carousel_images = CarouselImage.objects.filter(active=True)
    return render(request, 'gryb_app/home.html', {'carousel_images': carousel_images, 'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product=product)
    cart_form = CartForm()
    comment_form = CommentForm()
    return render(request, 'gryb_app/product_detail.html', {
        'product': product,
        'comments': comments,
        'cart_form': cart_form,
        'comment_form': comment_form
    })

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = Cart(user=request.user, item=product, quantity=quantity)
            cart.save()
            return redirect('gryb_app:cart')
    else:
        form = CartForm()
    return render(request, 'gryb_app/add_to_cart.html', {'form': form, 'product': product})


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'gryb_app/cart.html', {'cart_items': cart_items})


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    if request.method == 'POST':
        cart_item.delete()
        return redirect('gryb_app:cart')
    return render(request, 'gryb_app/remove_from_cart.html', {'cart_item': cart_item})

def thank_you(request):
    return render(request, 'gryb_app/thank_you.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                f'Contact Form Submission - {name}',
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return redirect('gryb_app:contact_thank_you')
    else:
        form = ContactForm()
    return render(request, 'gryb_app/contact.html', {'form': form})


def contact_thank_you(request):
    return render(request, 'gryb_app/contact_thank_you.html')


@login_required
def add_comment(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  
            comment.product = product
            comment.save()
            return redirect('gryb_app:product_detail', pk=product.pk)
    else:
        form = CommentForm()

    return render(request, 'gryb_app/add_comment.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'gryb_app/profile.html', {'user': request.user})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('gryb_app:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'gryb_app/edit_profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('gryb_app:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'gryb_app/change_password.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('gryb_app:home')

import logging

logger = logging.getLogger(__name__)

@login_required
def checkout(request):
    def get_cart_items_info(cart_items):
        cart_items_info = ""
        for item in cart_items:
            cart_items_info += f"{item.item.name} - Количество: {item.quantity}\n"
        return cart_items_info

    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.item.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            
            # Получаем первый товар из корзины
            first_item = cart_items.first()
            if first_item:
                order.item = first_item.item
            else:

                return redirect('empty_cart')  # Здесь 'empty_cart' - имя вашего представления для пустой корзины
            
            order.total = total
            order.save()

            send_mail(
                'New Order',
                f'Новый заказ\n\nПолучен новый заказ с информацией о заказчике, товарах и общей стоимости:\n\nИнформация о заказчике:\nИмя: {order.recipient_name}\nEmail: {order.recipient_email}\nНомер телефона: {order.recipient_phone}\nАдрес: {order.address}\n\nТовары в корзине:\n{get_cart_items_info(cart_items)}\n\nОбщая стоимость: {order.total}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.NOTIFICATION_EMAIL],
                fail_silently=False,
            )

            cart_items.delete()

            # Создание объекта HttpResponse
            response = HttpResponse(render(request, 'gryb_app/thank_you.html'))

            # Установка cookie
            response.set_cookie('cookie_name', 'cookie_value')

            return response
    else:
        form = OrderForm()

    return render(request, 'gryb_app/checkout.html', {'cart_items': cart_items, 'total': total, 'form': form})

def video_view(request):
    video = Video.objects.get(pk=1)  # Получение объекта видео из базы данных
    return render(request, 'gryb_app/home.html', {'video': video})

def abaut(request):
    return render(request, 'gryb_app/abaut.html')