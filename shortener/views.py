from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponseRedirect, HttpResponseGone
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from shortener.models import ShortUrl
from shortener.serializers import ShortenerSerializer
from utilities.http_code_handler import response_formatter
from utilities.log_redirects import create_redirect_log
from utilities.short_code_generator import suggested_short_code_validator, create_short_code

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class UrlShortenerAPI(mixins.CreateModelMixin, GenericViewSet):
    """
    <h2 style="color:blue">Create Url Shortener API</h2>

    Create url short code <br/>

    <br/>
    > Permission Scope: Only authenticated user can access this API
    """
    queryset = ShortUrl.objects.all()
    serializer_class = ShortenerSerializer

    def create(self, request, *args, **kwargs):
        serializer_data = request.data

        # Generate short code
        if serializer_data.get("suggested_short_code"):

            # Generate short code base on suggested short code
            serializer_data["short_code"] = suggested_short_code_validator(
                ShortUrl, serializer_data.get("suggested_short_code")
            )
            serializer_data.pop("suggested_short_code")
        else:
            serializer_data["short_code"] = create_short_code(ShortUrl)

        # Validate Serializer
        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        # Get created instance
        instance = self.perform_create(serializer)

        # Set cache
        cache.set(instance.get_short_url(), instance.url, timeout=CACHE_TTL)

        # Get success header
        headers = self.get_success_headers(serializer.data)

        # Return Response
        return Response(response_formatter(201, serializer.data), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        return serializer.save(user=self.request.user)


class RedirectAPI(APIView):
    """
    <h2 style="color:blue">Redirect API</h2>

    Redirect User to original url <br/>

    <br/>
    > Permission Scope: This api is public
    """
    permission_classes = (AllowAny,)

    def get_redirect_url(self, *args, **kwargs):
        # Check cache for short url
        cached_redirect_url = cache.get(self.request.build_absolute_uri())

        # If cache is found return it
        if cached_redirect_url:
            return cached_redirect_url

        # If cache is not found then search the database
        short_url_qs = ShortUrl.objects.filter(short_code=kwargs.get("short_code"))

        if short_url_qs.exists():
            # If there was a record in database then get it
            short_url_obj = short_url_qs.get()

            # Set cache
            cache.set(short_url_obj.get_short_url(), short_url_obj.url, timeout=CACHE_TTL)

            # Return url
            return short_url_obj.url

        # Return none if there was not url to redirect to
        return None

    def get(self, request, *args, **kwargs):
        # Get redirect url
        url = self.get_redirect_url(*args, **kwargs)

        if url:
            # Create log
            create_redirect_log(
                request.META.get("HTTP_USER_AGENT"),
                request.META.get("REMOTE_ADDR"),
                kwargs.get("short_code")
            )

            # Redirect if url is found
            return HttpResponseRedirect(url)
        else:
            # Return Gone response if there was no url
            return HttpResponseGone()
