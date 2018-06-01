from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models


def default_site():
    return Site.objects.get(id=settings.SITE_ID).id


class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at isn’t updated when making updates to other fields in other ways such as QuerySet.update()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserAuditAbstractModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(class)s_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
