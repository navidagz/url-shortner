from rest_framework import serializers

from shortener.models import ShortUrl
from url_shortener.settings import SHORT_CODE_MAX_LENGTH, SHORT_CODE_MIN_LENGTH
from utilities.baseSerializer import BaseModelSerializer


class ShortenerSerializer(BaseModelSerializer):
    """
    Shortener serializer
    """

    # Suggested short code is used if user wants to create custom short url
    suggested_short_code = serializers.CharField(
        max_length=SHORT_CODE_MAX_LENGTH,
        min_length=SHORT_CODE_MIN_LENGTH,
        write_only=True, required=False
    )

    short_url = serializers.SerializerMethodField()

    @staticmethod
    def get_short_url(obj):
        return obj.get_short_url()

    class Meta:
        model = ShortUrl
        fields = "__all__"
        ordering = ["-id"]
        read_only_fields = ["created_at", "updated_at", "viewed_count", "user"]
