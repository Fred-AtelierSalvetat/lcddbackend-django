from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from sortedm2m.fields import SortedManyToManyField


class Topic(models.Model):
    title = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to="topics/", blank=True)

    class Meta:
        verbose_name = "topic"
        ordering = ['id']

    def __str__(self):
        return self.title


class RefLegifrance(models.Model):
    ref = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.ref


class Workshop(models.Model):
    class Status(models.TextChoices):
        INCOMING = 'INCOMING', _('A venir')
        LIVE = 'LIVE', _('EN DIRECT')
        UNPUBLISHED = 'UNPUBLISHED', _('Inédit')
        PUBLISHED = 'PUBLISHED', _('Publié')
        ARCHIVED = 'ARCHIVED', _('Archivé')

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.INCOMING,
    )

    thumbnailUrl = models.CharField(max_length=255, blank=True)
    videoUrl = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=127)
    startingdate = models.DateTimeField()
    # speakers: [intervenants[0].value],
    topics = SortedManyToManyField(Topic)
    description = models.TextField()
    refsLegifrance = SortedManyToManyField(RefLegifrance, blank=True)

    # files: [],
    # links= models.SortedManyToManyField(Link, null= True)

    class Meta:
        verbose_name = "workshop"
        ordering = ['id']

    def __str__(self):
        return self.title


class Link(models.Model):
    label = models.CharField(max_length=127)
    url = models.URLField()
    workshop = models.ForeignKey(
        Workshop, related_name='links', on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.label, self.url)


class Keyword(models.Model):
    keyword = models.CharField(max_length=32)
    workshop = models.ForeignKey(
        Workshop, related_name='keywords', on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword


class Profession(models.Model):
    label = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.label


class UserProfile(models.Model):
    class Roles(models.TextChoices):
        SPEAKER_AWAITING_ANSWER = 'SPEAKER_AWAITING_ANSWER', _(
            'Speaker awaiting answer')
        SPEAKER_AWAITING_VALIDATION = 'SPEAKER_AWAITING_VALIDATION', _(
            'Speaker awaiting validation')
        SPEAKER = 'SPEAKER', _('Speaker')
        PROFESSIONAL = 'PROFESSIONAL', _('Professional')
        STUDENT = 'STUDENT', _('Student')
        CITIZEN = 'CITIZEN', _('Citizen')
        ADMIN = 'ADMIN', _('Admin')

    user = models.OneToOneField(
        User, related_name='userprofile', on_delete=models.CASCADE)
    lcdd_role = models.CharField(
        max_length=32, choices=Roles.choices, default=Roles.CITIZEN)
    city = models.CharField(max_length=100, default="")
    interests = SortedManyToManyField(Topic, blank=True)
    profession = models.ForeignKey(
        Profession, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32, blank=True)
    pro_email = models.EmailField(blank=True)
    bio_title = models.CharField(max_length=127, blank=True)
    biography = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self) -> str:
        return super().__str__()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
