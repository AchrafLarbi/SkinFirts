import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from doctor.models import Doctor, Specialization
from datetime import datetime

# Initialize Faker
fake = Faker()

# List of sample degrees
degrees = ["MD", "DO", "MBBS", "PhD"]

# List of sample available days and hours
available_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
available_hours = {
    "start_time": "09:00",
    "end_time": "17:00"
}

def create_doctors(num):
    specializations = Specialization.objects.all()
    for _ in range(num):
        specialization = random.choice(specializations)
        doctor = Doctor(
            name=fake.first_name(),
            lastname=fake.last_name(),
            degree=random.choice(degrees),
            specialization=specialization,
            begin_of_work=fake.date_between(start_date='-20y', end_date='-1y'),
            available_days={"day1": random.choice(available_days)},
            available_hours=available_hours,
            bio=fake.text(),
            highlights=fake.text()
        )
        doctor.save()

if __name__ == "__main__":
    num_doctors = 10  # Number of doctors to create
    create_doctors(num_doctors)
    print(f'{num_doctors} doctors created successfully.')
