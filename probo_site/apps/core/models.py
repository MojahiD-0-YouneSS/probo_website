from django.db import models

# Create your models here.

class MenuCategory(models.Model):
    """
    Categories like 'Starters', 'Main Courses', 'Desserts'.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display on the menu")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Menu Categories"

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    """
    Individual dishes.
    """
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Ingredients and allergens")

    # Store price as Decimal, not string (e.g. 12.00, not "$12")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Images (Requires Pillow installed)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    is_available = models.BooleanField(default=True,)
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (${self.price})"

# === CART MODELS (Temporary Storage) ===
class CartItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=250, null=True,blank=True)
    is_ordered = models.BooleanField(default=False)
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='items'
    )
    def subtotal(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

# === ORDER MODELS (Permanent Records) ===
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'pending'),
        ('Cooking', 'cooking'),
        ('Ready', 'ready'),
        ('Delivered', 'delivered'),
    ]

    # Order Info
    session_key = models.CharField(max_length=250, null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    cleared = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.total_price}$"

# === TABLE MODELS (Permanent Records) ===


class Table(models.Model):
    STATUS_CHOICES = [
        ('Availlable', 'availlable'),
        ('Cancelled', 'cancelled'),
        ('Delivered', 'delivered'),
    ]

    # Order Info
    session_key = models.CharField(max_length=250, null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Availlable')
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)
    booker_name = models.CharField(max_length=150, null=True,blank=True)
    booked_date = models.DateField(auto_now_add=True)
    booked_time = models.TimeField(auto_now_add=True)
    number_of_guests = models.IntegerField(default=2)
    def __str__(self):
        return f"table: {self.session_key}$"

