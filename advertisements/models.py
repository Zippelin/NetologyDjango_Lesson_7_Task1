from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='to_person')
    favorite_advertisement = models.ManyToManyField('Advertisement',
                                                    through='AdvertisementsUsers',
                                                    related_name='favorite_advertisements',
                                                    through_fields=('person', 'advertisement')
                                                    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Person.objects.create(user=instance)


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    persons_in_favorites = models.ManyToManyField(Person,
                                                  through='AdvertisementsUsers',
                                                  through_fields=('advertisement', 'person'),
                                                  related_name='persons_in_favorites')


class AdvertisementsUsers(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='relation_favorite'
    )
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='relation_favorite'
    )
    is_favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ['person', 'advertisement', 'is_favorite']