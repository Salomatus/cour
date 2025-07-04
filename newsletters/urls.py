from django.urls import path

from newsletters.apps import NewslettersConfig
from newsletters.views import base


app_name = NewslettersConfig.name


urlpatterns = [
    path("", base, name="base"),
]