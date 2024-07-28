import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')  # Replace 'myproject' with your project name
django.setup()

from doctor.models import Specialization  # Replace 'myapp' with your app name

# Initialize Faker
fake = Faker()

# List of sample specializations
specializations = [
    "Cardiology",
    "Dermatology",
    "Neurology",
    "Pediatrics",
    "Oncology",
    "Orthopedics",
    "Gynecology",
    "Urology",
    "Psychiatry",
    "Gastroenterology"
]

def create_specializations(num):
    for _ in range(num):
        specialization_name = random.choice(specializations)
        Specialization.objects.create(name=specialization_name)

if __name__ == "__main__":
    num_specializations = 10  # Number of specializations to create
    create_specializations(num_specializations)
    print(f'{num_specializations} specializations created successfully.')
