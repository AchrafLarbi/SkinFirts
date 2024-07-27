from rest_framework import serializers
from .models import Specialization, Doctor, Review, FavoriteDoctor
from users.models import User

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']


class DoctorSerializer(serializers.ModelSerializer):
    specialization = serializers.SlugRelatedField(slug_field='name', queryset=Specialization.objects.all())
    available_days = serializers.JSONField()
    available_hours = serializers.JSONField()
    
    # Make rating and reviews_count read-only
    rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()
    experience_years = serializers.ReadOnlyField()

    class Meta:
        model = Doctor
        fields = ['id','name','lastname', 'profile_picture', 'degree', 'specialization','begin_of_work', 'experience_years', 'rating', 'reviews_count', 'available_days', 'available_hours', 'bio', 'highlights']

class ReviewSerializer(serializers.ModelSerializer):
    doctor = serializers.SlugRelatedField(slug_field='id', queryset=Doctor.objects.all())
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    class Meta:
        model = Review
        fields = ['id', 'doctor', 'user', 'rating', 'comment']

class FavoriteDoctorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    doctor = serializers.SlugRelatedField(slug_field='id', queryset=Doctor.objects.all())

    class Meta:
        model = FavoriteDoctor
        fields = ['id', 'user', 'doctor']
