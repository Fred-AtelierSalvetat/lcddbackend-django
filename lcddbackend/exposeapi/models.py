from django.db import models

# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length= 100)
    thumbnail = models.CharField(max_length= 200)
    class Meta:
        verbose_name = "topic"
        ordering = ['id']

    def __str__(self):
        return self.title

# class Person(models.Model):
#     SHIRT_SIZES = (
#         ('S', 'Small'),
#         ('M', 'Medium'),
#         ('L', 'Large'),
#     )
#     name = models.CharField(max_length=60)
#     shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
