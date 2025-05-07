from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="districts")

    def __str__(self):
        return f"{self.name} ({self.state.name})"
class Taluk(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="taluks")

    def __str__(self):
        return f"{self.name} ({self.district.name})"

class RevenueVillage(models.Model):
    name = models.CharField(max_length=100)
    taluk = models.ForeignKey(Taluk, on_delete=models.CASCADE, related_name="revenue_villages")

    def __str__(self):
        return f"{self.name} ({self.taluk.name})"
from django.db import models
from django.contrib.auth.models import User
class Plot(models.Model):
    state = models.ForeignKey('State', on_delete=models.CASCADE, related_name='plots')
    district = models.ForeignKey('District', on_delete=models.CASCADE, related_name='plots')
    taluk = models.ForeignKey('Taluk', on_delete=models.CASCADE, related_name='plots')
    revenue_village = models.ForeignKey('RevenueVillage', on_delete=models.CASCADE, related_name='plots')
    owner = models.CharField(max_length=255)
    survey_no = models.CharField(max_length=100)
    subdivision = models.CharField(max_length=100, blank=True, null=True)
    plot_number = models.CharField(max_length=100, unique=True)
    dimensions = models.CharField(max_length=100)
    facing = models.CharField(max_length=100)
    price_range = models.CharField(max_length=100)
    land_image = models.ImageField(upload_to='land_images/', blank=True, null=True)  # Image field for land image

    def __str__(self):
        return f"Plot: {self.plot_number} ({self.owner})"
from django.db import models



from django.utils.timezone import now
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User owning the cart item
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)  # The plot added to the cart
    
    def __str__(self):
        return f"{self.user.username} ({self.plot.plot_number})"



from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the User model
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the order
    created_at = models.DateTimeField(default=timezone.now)
   

    def __str__(self):
        return f"Order {self.id} for {self.user}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem for Order {self.order.id}"
