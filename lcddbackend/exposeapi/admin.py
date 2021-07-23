from django.contrib import admin
from .models import Topic

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ( 'title',)
    search_fields = ('title', )
    ordering = ('id', )

admin.site.register(Topic, TopicAdmin)
