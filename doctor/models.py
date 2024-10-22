
from datetime import date
from django.db import models
from users.models import User

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

# Create your models here.
class Specialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    degree = models.CharField(max_length=255)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    begin_of_work = models.DateField() # Date when the doctor started working like 2021-01-01
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    # rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    rating = models.DecimalField(default=0.0, max_digits=3, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    reviews_count = models.PositiveIntegerField(default=0)
    available_days = models.JSONField(blank=True, null=True) # {day: 'day_name'}
    available_hours = models.JSONField(blank=True,null=True) # {day: {start: 'hh:mm', end: 'hh:mm'}}
    bio = models.TextField(blank=True)
    highlights = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.name} ,{self.lastname}, {self.degree}"

    def update_rating_and_review_count(self):
        reviews = self.reviews.all()
        if reviews:
            self.reviews_count = reviews.count()
            self.rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
        else:
            self.reviews_count = 0
            self.rating = 0.0
        self.save()

    def calculate_experience_years(self):
        today = date.today()
        self.experience_years = abs(today.year - self.begin_of_work.year)

    def save(self, *args, **kwargs):
        self.calculate_experience_years()
        super().save(*args, **kwargs)

    # Update doctor rating and review count whenever a review is deleted


class Review(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Review for {self.doctor} by {self.user}"

    # Update doctor rating and review count whenever a review is saved
    @receiver(post_save, sender='doctor.Review')
    def update_doctor_rating_and_review_count(sender, instance, **kwargs):
        instance.doctor.update_rating_and_review_count()

class FavoriteDoctor(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='favorited_by', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'doctor')

    def __str__(self):
        return f"{self.user} favorited {self.doctor}"
