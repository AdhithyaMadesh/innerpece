from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()




class Tour(models.Model):
    CATEGORY_CHOICES = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'),
        ('category3', 'Category 3'),
    ]

    CHECKBOX_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
        ('option5', 'Option 5'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    keyword = models.CharField(max_length=255)
    description = models.TextField()
    day1 = models.TextField()
    day2 = models.TextField()
    day3 = models.TextField()
    location = models.CharField(max_length=255)
    checkboxes = models.JSONField(default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.title} {self.date} {self.time}"

class TourPhoto(models.Model):
    tour = models.ForeignKey(Tour, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='tour_photos/')
