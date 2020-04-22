from django.db import models

from url_shortener.settings import SHORT_CODE_MAX_LENGTH, BASE_SHORT_URL


class ShortUrl(models.Model):
    """
    ShortUrl model
    """
    url = models.URLField()
    short_code = models.CharField(max_length=SHORT_CODE_MAX_LENGTH, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey("authentication.User", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.url} -----> {self.get_short_url()}"

    def get_short_url(self):
        """
        Return short url
        :return:
        """
        return BASE_SHORT_URL.format(self.short_code)
