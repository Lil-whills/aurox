from django.conf import settings
from django.db import models

# Create your models here.
class Properties(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=[('house', 'House'), ('apartment', 'Apartment'), ('condo', 'Condo'), ('hotel', 'Hotel'), ('estate', 'Estate'), ('villa', 'Villa'), ('cottage', 'Cottage'), ('penthouse', 'Penthouse')])
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    description = models.TextField()
    image1 = models.ImageField(upload_to='property_images/')
    image2 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    virtual_tour_url = models.URLField(max_length=500, blank=True)
    status = models.CharField(max_length=50, choices=[('available', 'Available'), ('sold', 'Sold'), ('not_available', 'Not Available')])
    category = models.CharField(max_length=50, choices=[('for_sale', 'For Sale'), ('for_rent', 'For Rent')])
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SavedProperty(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_properties',
    )
    property = models.ForeignKey(
        Properties,
        on_delete=models.CASCADE,
        related_name='saved_by_users',
    )
    is_paid = models.BooleanField(default=False)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-saved_at',)
        constraints = [
            models.UniqueConstraint(fields=('user', 'property'), name='unique_saved_property_per_user'),
        ]

    def __str__(self):
        return f'{self.user} saved {self.property}'