from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter

from shortener.views import UrlShortenerAPI

router = SimpleRouter()

# Short url create route
router.register('', UrlShortenerAPI, "shortener")

urlpatterns = [
    # Add router urls
    url(r'', include(router.urls)),
]
