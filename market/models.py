import decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(null=False, blank=False, unique=True)
    phone_number = models.CharField(unique=True, blank=False, null=False, max_length=50)
    avatar = models.ImageField(upload_to='upload/%Y/%m', null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    balance = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(decimal.Decimal('0.01'))], default=0.01)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    is_business = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name + " - " + str(self.id)


class Address(models.Model):
    # Using GHN API Address for province_id, district_id, ward_id
    country = models.CharField(max_length=100, default="Viet Nam")
    province_id = models.IntegerField(blank=False, null=False)
    district_id = models.IntegerField(blank=False, null=False)
    ward_id = models.CharField(max_length=255, blank=False, null=False)
    street = models.CharField(max_length=255)
    full_address = models.TextField(default="ABC")
    note = RichTextField(blank=True, null=True)
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.full_address


class Report(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    subject = models.TextField()
    content = RichTextField()

    STATUS_CHOICE = (
        (0, 'pending'),
        (1, 'checked'),
        (2, 're_apply'),
        (3, 'done')
    )

    status = models.IntegerField(choices=STATUS_CHOICE, default=0)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.subject


class Reply(models.Model):
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    is_available = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category)
    sold_amount = models.BigIntegerField(default=0)
    picture = models.ImageField(upload_to='night_owl/product', null=True, blank=True)
    description = RichTextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='sold_amount_positive',
                check=models.Q(sold_amount__gte=0)
            )
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def min_price(self):
        return Option.objects.filter(base_product=self).aggregate(models.Min('price')).get('price__min')


    def save(self, *args, **kwargs):
        if not self.owner.is_business:
            raise ValidationError('owner is not business')
        super().save(*args, **kwargs)


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    can_destroy = models.BooleanField(default=True)
    completed_date = models.DateField(null=True)
    shipping_code = models.CharField(max_length=255, blank=True, null=True)
    total_shipping_fee = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    note = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customer_order')
    store = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='store_order')
    voucher_apply = models.ForeignKey('Voucher', on_delete=models.SET_NULL, null=True)

    STATUS_CHOICES = (
        (0, 'UnCheckout'),
        (1, 'Approving'),
        (2, 'Pending'),
        (3, 'Completed'),
        (4, 'Canceled'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    SHIPPING_CHOICES = (
        (0, 'COD'),
        (1, 'OnlinePaymentWithMomo'),
        (2, 'PaymentWithNightOwlAmount')
    )
    payment_type = models.IntegerField(choices=SHIPPING_CHOICES, default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='positive_total_shipping_fee',
                check=models.Q(total_shipping_fee__gte=0)
            )
        ]

    def save(self, *args, **kwargs):
        if self.store and self.customer and self.store.id == self.customer.id:
            raise ValidationError(message="Store cannot buy their product")
        else:
            super().save(*args, **kwargs)


class Option(models.Model):
    unit = models.CharField(max_length=255, blank=False, null=False)
    unit_in_stock = models.PositiveBigIntegerField(default=1, null=False, blank=False)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    weight = models.PositiveIntegerField(default=1)
    height = models.PositiveIntegerField(default=1)
    width = models.PositiveIntegerField(default=1)
    length = models.PositiveIntegerField(default=1)

    base_product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.base_product.name + " " + self.unit

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='min_option_price_constraint',
                check=models.Q(price__gte=decimal.Decimal(1))
            ),
            models.CheckConstraint(
                name='min_dimension_and_weight_option_constraint',
                check=models.Q(weight__gte=1, height__gte=1, length__gte=1, width__gte=1)
            )
        ]


class Picture(models.Model):
    image = models.ImageField(upload_to='night_owl/product')
    product_option = models.ForeignKey(Option, on_delete=models.CASCADE)


class OrderDetail(models.Model):
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product_option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    cart_id = models.ForeignKey('CartDetail', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='min_order_detail_unit_price',
                check=models.Q(unit_price__gte=1)
            ),
            models.CheckConstraint(
                name='min_order_detail_quantity',
                check=models.Q(quantity__gte=1)
            )
        ]

    def save(self, *args, **kwargs):
        if self.quantity > self.product_option.unit_in_stock:
            raise ValidationError('not enough unit in stock')
        super().save(*args, **kwargs)


class Bill(models.Model):
    value = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    payed = models.BooleanField(default=False, null=False, blank=False)
    order_payed = models.OneToOneField(Order, on_delete=models.CASCADE, default=False)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Order Id: " +  str(self.order_payed.id)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='bill_min_value_constraint',
                check=models.Q(value__gte=decimal.Decimal(0))
            )
        ]


class CartDetail(models.Model):
    quantity = models.PositiveIntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_option = models.ForeignKey(Option, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['customer', 'product_option']]
        constraints = [
            models.CheckConstraint(
                name='cart_quantity_constr',
                check=models.Q(quantity__gte=1)
            ),
        ]

    def save(self, *args, **kwargs):
        if self.customer.id == self.product_option.base_product.owner_id:
            raise ValidationError(message="store cannot add their product to their cart")
        else:
            super().save(*args, **kwargs)


class Rating(models.Model):
    rate = models.PositiveIntegerField()
    comment = RichTextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.creator.first_name + " rated " + self.product.name + "\t" + str(self.rate)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='rate_range_constraint',
                check=models.Q(rate__lte=5, rate__gte=1)
            )
        ]

    def save(self, *args, **kwargs):
        if not Order.objects.filter(customer=self.creator, orderdetail__product_option__base_product=self.product).exists():
            raise ValidationError(message='Customer must buy product before rating')
        super().save(*args, **kwargs)

class Voucher(models.Model):
    discount = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    code = models.CharField(default='nightowl', unique=True, max_length=24)
    is_percentage = models.BooleanField(default=False)
    products = models.ManyToManyField(Product)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='percentage_voucher_constraint',
                check=models.Q(is_percentage=False) | (models.Q(is_percentage=True) & models.Q(discount__lte=decimal.Decimal(100)))
            ),
            models.CheckConstraint(
                name='min_discount_constraint',
                check=models.Q(discount__gte=decimal.Decimal(0.01))
            ),
            models.CheckConstraint(
                name='voucher_end_date_gte_start_date_constraint',
                check=models.Q(end_date__isnull=True) | models.Q(end_date__gt=models.F('start_date'))
            )
        ]