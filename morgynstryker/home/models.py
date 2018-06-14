from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404

from utils.models import default_site, UserAuditAbstractModel


class About(UserAuditAbstractModel):
    header = models.CharField(max_length=100, default='About Me')
    description = models.TextField(null=False)
    default = models.BooleanField(default=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=default_site)

    class Meta:
        verbose_name_plural = 'about'

    # @classmethod
    # def get_or_404(cls, request):
    #     """Get the default description for the current site
    #
    #     Returns: Single object
    #
    #     """
    #     try:
    #         obj = About.objects.get(default=True, site__id=get_current_site(request).id)
    #     except cls.DoesNotExist:
    #         raise Http404('About content not found.')
    #     return obj

    def _update_default(self):
        """Query all values for this site that may have been set to default if
        the current object being saved is set as the default.

        Returns: None

        """
        if not self.default:
            return

        objs = About.objects.filter(site_id=settings.SITE_ID, default=True)
        if objs.count() == 0:
            return

        if self.pk:
            objs = objs.exclude(pk=self.pk)

        # change any object that was set to default True to False
        objs.update(default=False)

    def clean(self):
        self._update_default()
