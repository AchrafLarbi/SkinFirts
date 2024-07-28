from rest_framework import viewsets
from .models import Specialization, Doctor, Review, FavoriteDoctor
from .serializers import FavoriteDoctorListSerializer, SpecializationSerializer, DoctorSerializer, ReviewSerializer, FavoriteDoctorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SpecializationSerializer(queryset, many=True)
        if not serializer.data:
            error_response = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "errorMessage": "No specializations found"
                }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SpecializationSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SpecializationSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DoctorSerializer(queryset, many=True, context=self.get_serializer_context())
        if not serializer.data:
            error_response = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "errorMessage": "No doctors found"
                }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ReviewSerializer(queryset, many=True)
        if not serializer.data:
            error_response = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "errorMessage": "No reviews found"
                }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

# class FavoriteDoctorViewSet(viewsets.ModelViewSet):
#     queryset = FavoriteDoctor.objects.all()
#     serializer_class = FavoriteDoctorSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = FavoriteDoctorSerializer(queryset, many=True)
#         if not serializer.data:
#             error_response = {
#                     "status": status.HTTP_404_NOT_FOUND,
#                     "errorMessage": "No favorite doctors found"
#                 }
#             return Response(error_response, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def create(self, request, *args, **kwargs):
#         serializer = FavoriteDoctorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             error_messages = []
#             for field, errors in serializer.errors.items():
#                 for error in errors:
#                     error_messages.append(f"{field}: {error}")
#             error_message_str = " ".join(error_messages)
            
#             error_response = {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "errorMessage": error_message_str
#             }
#             return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

class FavoriteDoctorViewSet(viewsets.ModelViewSet):
    queryset = FavoriteDoctor.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return FavoriteDoctorListSerializer
        return FavoriteDoctorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        # Eliminate duplicates at the application level
        seen_doctors = set()
        unique_favorites = []
        for favorite in queryset:
            if favorite.doctor_id not in seen_doctors:
                unique_favorites.append(favorite)
                seen_doctors.add(favorite.doctor_id)
        serializer = self.get_serializer(unique_favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor')
        if FavoriteDoctor.objects.filter(user=request.user, doctor_id=doctor_id).exists():
            return Response({'detail': 'This doctor is already in your favorites.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)

            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete/(?P<doctor_id>\d+)')
    def delete_favorite(self, request, doctor_id=None):
        try:
            favorite = FavoriteDoctor.objects.get(user=request.user, doctor_id=doctor_id)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FavoriteDoctor.DoesNotExist:
            return Response({'detail': 'Favorite not found.'}, status=status.HTTP_404_NOT_FOUND)
