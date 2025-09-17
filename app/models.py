from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

#  Custom User Manager 
class CustomUserManager(BaseUserManager):
    def create_user(self, email, cpf, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser informado')
        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, cpf, first_name, last_name, password, **extra_fields)

#  Custom User 
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=12, unique=True)
    address_country = models.CharField(max_length=150)
    address_state = models.CharField(max_length=150)
    address_city = models.CharField(max_length=150)
    address_district = models.CharField(max_length=150)
    address_street = models.CharField(max_length=150)
    address_zip_code = models.CharField(max_length=15)
    address_number = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'first_name', 'last_name']

    objects = CustomUserManager()

#  Category 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

#  Product 
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    total_reviews = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

#  ProductPiece 
class ProductPiece(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pieces')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    measurements = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

#  ProductImage 
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    is_main = models.BooleanField(default=False)

#  Order 
class Order(models.Model):
    PAYMENT_METHODS = [
        ('PIX', 'PIX'),
        ('BOLETO', 'Boleto'),
        ('CARD', 'Cartão de Crédito'),
    ]

    STATUS_CHOICES = [
        ('PROCESSING', 'EM PROCESSAMENTO'),
        ('PAID', 'PAGAMENTO APROVADO'),
        ('INVOICE', 'NOTA FISCAL EMITIDA'),
        ('PREPARING', 'EM PREPARAÇÃO'),
        ('SENT', 'ENVIADO'),
        ('RECEIVED', 'RECEBIDO'),
        ('PAYMENT_FAILED', 'PAGAMENTO REPROVADO'),
        ('CANCELED', 'CANCELADO'),
        ('RETURN_REQUEST', 'SOLICITAÇÃO DE DEVOLUÇÃO'),
        ('RETURNING', 'EM DEVOLUÇÃO'),
        ('RETURNED', 'DEVOLVIDO'),
        ('RETURN_CANCELED', 'DEVOLUÇÃO CANCELADA'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=15, decimal_places=2)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PROCESSING')
    tracking_code = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

#  OrderItem 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

#  CreditCard 
class CreditCard(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='credit_card')
    card_number = models.CharField(max_length=20)
    expiration_date = models.CharField(max_length=10)
    holder_name = models.CharField(max_length=255)
    cvv = models.CharField(max_length=5)

#  ProductReview 
class ProductReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
