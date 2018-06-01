from django.contrib import admin

from .models import About


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fields = [
        'default',
        'header',
        'description',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    ]
    list_display = [
        'default',
        'header',
        'description',
        'site',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    ]
    readonly_fields = [
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    ]

    def short_description(self, obj):
        # Get the first 50 characters of the description and add "..." to the end
        if len(obj.description) > 50:
            return '{description}...'.format(description=obj.description[:50])

        return obj.description

    short_description.empty_value_display = '???'

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'created_by'):
            obj.created_by = request.user

        obj.updated_by = request.user
        obj.save()
