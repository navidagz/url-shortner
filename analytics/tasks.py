import json
import shutil
from datetime import datetime
from os import listdir, path, mkdir

import user_agents
from celery import shared_task

from analytics.models import Analytics, Browser, Device
from shortener.models import ShortUrl
from url_shortener.settings import LOG_ROOT_DIR, ANALYZED_LOG_DIR, ANALYZED_LOG_DIR_NAME, BASE_LOG_FILE, DATE_TIME_FORMAT


@shared_task
def create_analytic():
    """
    Create analytics
    First new log files gets created then this function gets called
    :return:
    """
    log_files = sorted(listdir(LOG_ROOT_DIR))

    if not path.isdir(ANALYZED_LOG_DIR):
        mkdir(ANALYZED_LOG_DIR)

    # Don't process base log file and analyzed folder
    if (ANALYZED_LOG_DIR_NAME in log_files) and (BASE_LOG_FILE in log_files) and (len(log_files) == 2):
        return

    file_name = LOG_ROOT_DIR + log_files[-1]

    # First new log file gets created so one before last file is used
    with open(file_name, "r") as f:
        # Get log infos from file in json format
        file_info = [
            json.loads(item)
            for item in
            list(map(lambda data: data.split("\n")[0], f.readlines()))
        ]

        # Iterate over logs
        for info in file_info:

            # Check for short code in db
            short_url_qs = ShortUrl.objects.filter(short_code=info.get("short_code"))
            if short_url_qs.exists():
                short_url_obj = short_url_qs.get()

                # Create analytics for the code
                analytics_obj, created = Analytics.objects.get_or_create(
                    shortener=short_url_obj
                )

                # Get user agent info such as browser and device
                user_agent_info = user_agents.parse(info.get("user_agent"))

                # Get remote address
                remote_addr = info.get("remote_addr")

                # Get crated at field
                created_at = datetime.strptime(info.get("created_at"), DATE_TIME_FORMAT)

                # Create browser object
                browser_obj = Browser.objects.create(
                    name=user_agent_info.browser.family,
                    remote_addr=remote_addr,
                    created_at=created_at
                )

                # Add browser object to analytics
                analytics_obj.browsers.add(browser_obj)

                # Check for user agent device
                if user_agent_info.is_pc:
                    device_type = Device.DESKTOP
                elif user_agent_info.is_mobile:
                    device_type = Device.MOBILE
                else:
                    device_type = Device.OTHER

                # Create device object
                device_obj = Device.objects.create(
                    device_type=device_type,
                    remote_addr=remote_addr,
                    created_at=created_at
                )

                # Add device device to analytics
                analytics_obj.devices.add(device_obj)

                # Save analytics
                analytics_obj.save()

    # Move log file to analyzed folder
    shutil.move(file_name, ANALYZED_LOG_DIR)
