from collections import OrderedDict

from django.db import models
from django.db.models import Count
from django.utils import timezone


class Analytics(models.Model):
    """
    Analytics model
    """
    shortener = models.ForeignKey("shortener.ShortUrl", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    devices = models.ManyToManyField("analytics.Device", blank=True)
    browsers = models.ManyToManyField("analytics.Browser", blank=True)

    def __str__(self):
        return f"{self.shortener.get_short_url()}"

    @staticmethod
    def filter_time(qs, time=None):
        """
        Filter queryset based on time given
        :param qs:
        :param time:
        :return:
        """
        today_midnight_date_time = timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)

        if time == "today":
            time_less_than = timezone.localtime(timezone.now())
            time_greater_than = today_midnight_date_time
        elif time == "yesterday":
            time_less_than = today_midnight_date_time - timezone.timedelta(minutes=1)
            time_greater_than = today_midnight_date_time - timezone.timedelta(days=1)
        elif time == "week":
            time_less_than = today_midnight_date_time - timezone.timedelta(minutes=1)
            time_greater_than = today_midnight_date_time - timezone.timedelta(days=7)
        elif time == "month":
            time_less_than = today_midnight_date_time - timezone.timedelta(minutes=1)
            time_greater_than = today_midnight_date_time - timezone.timedelta(days=30)
        else:
            return qs

        return qs.filter(created_at__gte=time_greater_than, created_at__lt=time_less_than)

    def all_views(self, time):
        """
        Get all views count
        :param time:
        :return:
        """
        return self.filter_time(self.devices, time).count()

    def device_views(self, time):
        """
        Get views base on device
        :param time:
        :return:
        """
        device_views_dict = OrderedDict()

        for device in self.filter_time(self.devices.values("device_type").annotate(count=Count("device_type")).distinct(), time):
            device_views_dict[device.get("device_type")] = device.get("count")

        return device_views_dict

    def browser_views(self, time):
        """
        Get views base browser
        :param time:
        :return:
        """
        browser_views_dict = OrderedDict()

        for browser in self.filter_time(self.browsers.values("name").annotate(count=Count("name")).distinct(), time):
            browser_views_dict[browser.get("name")] = browser.get("count")

        return browser_views_dict

    def unique_user_views(self, time):
        """
        Get user unique view count
        :param time:
        :return:
        """
        return self.filter_time(self.devices.values("remote_addr").distinct(), time).count()

    def unique_user_device_views(self, time):
        """
        Get user unique view count base on device
        :param time:
        :return:
        """
        unique_user_device_views_dict = OrderedDict()
        unique_name_list = self.filter_time(self.devices.distinct("device_type"), time).values_list("device_type", flat=True)

        for device_type in unique_name_list:
            unique_user_device_views_dict[device_type] = self.filter_time(self.devices.distinct(
                "device_type", "remote_addr").filter(device_type=device_type), time).count()

        return unique_user_device_views_dict

    def unique_user_browser_views(self, time):
        """
        Get user unique view count base on browser
        :param time:
        :return:
        """
        unique_user_browser_views_dict = OrderedDict()
        unique_name_list = self.filter_time(self.browsers.distinct("name"), time).values_list("name", flat=True)

        for name in unique_name_list:
            unique_user_browser_views_dict[name] = self.filter_time(self.browsers.distinct(
                "name", "remote_addr").filter(name=name), time).count()

        return unique_user_browser_views_dict


class Browser(models.Model):
    """
    Browser Model
    """
    name = models.TextField("browser_name")
    remote_addr = models.GenericIPAddressField("remote_addr")

    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ----> {self.remote_addr}"


class Device(models.Model):
    """
    Device Model
    """
    DESKTOP = "Desktop"
    MOBILE = "Mobile"
    OTHER = "Other"

    DEVICE_TYPES = (
        (DESKTOP, DESKTOP),
        (MOBILE, MOBILE),
        (OTHER, OTHER)
    )

    device_type = models.CharField(max_length=7, choices=DEVICE_TYPES)
    remote_addr = models.GenericIPAddressField("remote_addr")

    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.device_type} -----> {self.remote_addr}"
