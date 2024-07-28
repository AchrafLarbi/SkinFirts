import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from doctor.models import FavoriteDoctor, Doctor
from users.models import User

# Initialize Faker
fake = Faker()

def create_favorite_doctors(num):
    doctors = Doctor.objects.all()
    users = User.objects.all()
    for _ in range(num):
        doctor = random.choice(doctors)
        user = random.choice(users)
        favorite = FavoriteDoctor(
            doctor=doctor,
            user=user
        )
        favorite.save()

if __name__ == "__main__":
    num_favorites = 15  # Number of favorite doctors to create
    create_favorite_doctors(num_favorites)
    print(f'{num_favorites} favorite doctors created successfully.')
