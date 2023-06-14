from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager, Group as AuthGroup, Permission as AuthPermission
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager


class CarouselImage(models.Model):
    image = models.ImageField('Изображение', upload_to='carousel_images/')
    active = models.BooleanField('Активность', default=False)
    link = models.URLField('Ссылка', blank=True)
    text = models.CharField('Текст на слайде', max_length=255, blank=True)
    button_text = models.CharField('Текст на кнопке', max_length=255, blank=True)

    def __str__(self):
        return str(self.id)

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = email
        extra_fields.setdefault('email', email)
        extra_fields.setdefault('username', username)
        return self.model(**extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self._create_user(email=email, password=password, **extra_fields)
        return user


class User(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=150, unique=True, blank=True, null=True)
    name = models.CharField('Имя', max_length=255)
    email = models.EmailField('Email', unique=True)
    phone_number = models.CharField('Номер телефона', max_length=20)
    address = models.CharField('Адрес', max_length=255)
    groups = models.ManyToManyField(AuthGroup, blank=True, related_name='gryb_users')
    user_permissions = models.ManyToManyField(AuthPermission, blank=True, related_name='gryb_users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'address']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Product(models.Model):
    name = models.CharField('Наименование', max_length=255)
    image = models.ImageField('Изображение', upload_to='product_images/')
    group = models.CharField('Группа', max_length=100)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    description = models.TextField('Описание', null=True)
    compound = models.TextField('Состав', null=True)
    application = models.TextField('Показания к применению', null=True)
    contraindications = models.TextField('Противопоказания', null=True)
    doza = models.TextField('Способ приминения и дозировка', null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart - User: {self.user.username}, Item: {self.item.name}, Quantity: {self.quantity}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    recipient_name = models.CharField(max_length=100)
    recipient_name = models.CharField('Имя получателя', max_length=255, default='Null')
    recipient_email = models.EmailField('Email получателя', default='Null')  
    recipient_phone = models.CharField('Номер телефона получателя', max_length=20, default='Null')
    address = models.CharField('Адрес доставки', max_length=255, default='Самовывоз с. Алматы')

    def __str__(self):
        return f'Order {self.pk}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Comment by {self.user.email} on {self.product.name}"
    
    # superuser = CustomUserManager().create_superuser(email='admin@example.com', password='password')

