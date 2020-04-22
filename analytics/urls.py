from django.conf.urls import url

from analytics.views import AnalyticsAPI

urlpatterns = [
    url(r'', AnalyticsAPI.as_view(), name="analytics"),
]
