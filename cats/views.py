from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema


from .models import Achievement, Cat, Review, Breed

from .serializers import (
    AchievementSerializer, CatSerializer, ReviewSerializer, BreedSerializer
)
from .permissions import IsAdminModeratorAuthorOrReadOnly


class CatViewSet(viewsets.ModelViewSet):
    """Viewset для модели Котов."""

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        operation_summary='Создание нового котенка',
        responses={
            201: CatSerializer(),
            400: 'Неверные данные',
            401: 'Не авторизован'
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AchievementViewSet(viewsets.ModelViewSet):
    """Viewset для модели Достижений."""

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None

    @swagger_auto_schema(
        operation_summary='Создать новое достижение',
        operation_description='Создает новое достижение с указанными данными.',
        request_body=AchievementSerializer,
        responses={
            201: AchievementSerializer(),
            400: 'Неверные данные',
            401: 'Не авторизован'
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для модели Отзывов."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )

    @swagger_auto_schema(
        operation_summary='Создание отзыва',
        responses={
            201: ReviewSerializer(),
            400: 'Неверные данные',
            401: 'Не авторизован'
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class BreedViewSet(viewsets.ModelViewSet):
    """ViewSet модели пород."""

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Получение списка всех пород',
        responses={
            201: BreedSerializer(),
            400: 'Неверные данные',
            401: 'Не авторизован'
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
