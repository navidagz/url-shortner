from rest_framework import serializers

from analytics.models import Analytics
from utilities.baseSerializer import BaseModelSerializer


class AnalyticsSerializer(BaseModelSerializer):
    """
    Analytic sSerializer
    """
    all_views = serializers.SerializerMethodField()
    device_views = serializers.SerializerMethodField()
    browser_views = serializers.SerializerMethodField()

    unique_user_views = serializers.SerializerMethodField()
    unique_user_device_views = serializers.SerializerMethodField()
    unique_user_browser_views = serializers.SerializerMethodField()

    def time_query_param(self):
        """
        Return time query param
        :return:
        """
        return self.context.get("request").query_params.get("time")

    def get_all_views(self, obj):
        return obj.all_views(self.time_query_param())

    def get_device_views(self, obj):
        return obj.device_views(self.time_query_param())

    def get_browser_views(self, obj):
        return obj.browser_views(self.time_query_param())

    def get_unique_user_views(self, obj):
        return obj.unique_user_views(self.time_query_param())

    def get_unique_user_device_views(self, obj):
        return obj.unique_user_device_views(self.time_query_param())

    def get_unique_user_browser_views(self, obj):
        return obj.unique_user_browser_views(self.time_query_param())

    class Meta:
        model = Analytics
        ordering = ["-id"]
        fields = [
            "all_views", "device_views", "browser_views",
            "unique_user_views", "unique_user_device_views", "unique_user_browser_views"
        ]
