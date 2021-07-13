from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, \
    AbstractBaseUser
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and save a new user"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates a new super user"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=300)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Product(models.Model):
    """Product object"""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stockQuantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return f'{self.id} {self.name}'


class Order(models.Model):
    """Order made by an user"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField('Product')
    orderDate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f'{self.id}'


class Payment(models.Model):
    """Payment made on a order"""
    value = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now=True)
    orders = models.ManyToManyField('Order')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f'{self.id}'


class Shipment(models.Model):
    """Shipment for an order"""
    sent_date = models.DateTimeField(null=True)
    received_date = models.DateTimeField(null=True)
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'shipment'

    def __str__(self):
        return f'{self.id}'
