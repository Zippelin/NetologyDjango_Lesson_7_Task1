from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.serializers import AdvertisementSerializer, AdvertisementsUsersSerializer
from .filters import AdvertisementFilter

from .permissions import IsAdvertisementOwnerOrAdmin


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdvertisementOwnerOrAdmin()]
        return []

    def get_queryset(self):
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            return super().get_queryset().filter(
                ~Q(status=AdvertisementStatusChoices.DRAFT) |
                Q(status__contains='') & Q(creator=self.request.user)
            )
        elif self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().exclude(status=AdvertisementStatusChoices.DRAFT)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated], url_path='favorite')
    def add_favorite(self, request, pk=None):

        serializer = AdvertisementsUsersSerializer(data={'person': request.user.to_person.id,
                                                         'advertisement': pk,
                                                         'is_favorite': True
                                                         })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='favorite-list')
    def get_favorite(self, request, pk=None):
        serializer = self.get_serializer(Advertisement.objects.filter(
            creator=request.user.to_person,
            relation_favorite__is_favorite=True), many=True)
        return Response(serializer.data)