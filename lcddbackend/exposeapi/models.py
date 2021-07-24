from django.db import models
from django.utils.translation import gettext_lazy as _

class Topic(models.Model):
    title = models.CharField(max_length= 100, unique=True)
    thumbnail = models.CharField(max_length= 255)
    class Meta:
        verbose_name = "topic"
        ordering = ['id']

    def __str__(self):
        return self.title


class RefLegifrance(models.Model):
    ref= models.CharField(max_length= 32, unique=True)
    
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

    thumbnailUrl = models.CharField(max_length= 255, blank=True)
    videoUrl = models.CharField(max_length= 255, blank=True)
    title= models.CharField(max_length= 127)
    startingdate = models.DateTimeField()
    #speakers: [intervenants[0].value],
    topics = models.ManyToManyField(Topic)
    description = models.TextField()
    refsLegifrance = models.ManyToManyField(RefLegifrance, blank=True)

    # files: [],
    #links= models.ManyToManyField(Link, null= True)

    class Meta:
        verbose_name = "workshop"
        ordering = ['id']

    def __str__(self):
        return self.title


class Link(models.Model):
    label= models.CharField(max_length= 127)
    url= models.URLField()
    workshop = models.ForeignKey(Workshop, related_name='links', on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s: %s' % (self.label, self.url)

class Keyword(models.Model):
    keyword= models.CharField(max_length= 32)
    workshop = models.ForeignKey(Workshop, related_name='keywords', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.keyword
