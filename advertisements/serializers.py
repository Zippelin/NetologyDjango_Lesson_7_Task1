from rest_framework import serializers

from advertisements.models import Advertisement, Person, AdvertisementsUsers


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = Person
        fields = ('id', 'user')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)
        depth = 1

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user.to_person
        if Advertisement.objects.filter(creator=validated_data["creator"]).count() == 10:
            raise serializers.ValidationError('Нельзя создавать больше 10 объявлений')
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        return data


class AdvertisementsUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvertisementsUsers
        fields = ('is_favorite', 'advertisement', 'person')