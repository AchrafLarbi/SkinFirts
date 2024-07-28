import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from doctor.models import Review, Doctor
from users.models import User

# Initialize Faker
fake = Faker()

def create_reviews(num):
    doctors = Doctor.objects.all()
    users = User.objects.all()
    for _ in range(num):
        doctor = random.choice(doctors)
        user = random.choice(users)
        review = Review(
            doctor=doctor,
            user=user,
            rating=random.uniform(1.0, 5.0),
            comment=fake.text()
        )
        review.save()
        doctor.update_rating_and_review_count()  # Update the doctor's rating and review count

if __name__ == "__main__":
    num_reviews = 60  # Number of reviews to create
    create_reviews(num_reviews)
    print(f'{num_reviews} reviews created successfully.')
