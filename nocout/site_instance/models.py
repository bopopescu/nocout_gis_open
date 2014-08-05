from django.db import models
from machine.models import Machine


class SiteInstance(models.Model):
    """
    Site Instance Model Columns Declaration.
    """
    name = models.CharField('Name', max_length=200, unique=True)
    alias = models.CharField('Alias', max_length=255)
    machine = models.ForeignKey(Machine, null=True, blank=True)
    live_status_tcp_port = models.IntegerField('Live Status TCP Port', null=True, blank=True)
    web_service_port = models.IntegerField('Web Service Port', default=80)
    username = models.CharField('Username', max_length=100, null=True, blank=True)
    password = models.CharField('Password', max_length=100, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)

    def __unicode__(self):
        """
        Site Instance objects presentation.
        """
        return self.name