#To register the SiteInstance for the admin.
from django.contrib import admin
from site_instance.models import SiteInstance

admin.site.register(SiteInstance)
