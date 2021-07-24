from django.contrib import admin
from .models import Keyword, Link, RefLegifrance, Topic, Workshop

admin.site.register(Topic)
admin.site.register(RefLegifrance)

class KeywordInline(admin.TabularInline):
    model = Keyword

class LinkInline(admin.TabularInline):
    model = Link

class WorkshopAdmin(admin.ModelAdmin):
    model = Workshop
    inlines = [
        KeywordInline,
        LinkInline,
    ]


admin.site.register(Workshop, WorkshopAdmin)
