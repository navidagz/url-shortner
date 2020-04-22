import json

from django.utils import timezone

from url_shortener.settings import DATE_TIME_FORMAT
from utilities.logging_config import get_logger


def create_redirect_log(user_agent, remote_addr, short_code):
    """
    Shared Task
    Create redirect log and save to file
    :param user_agent:
    :param remote_addr:
    :param short_code:
    :return:
    """
    try:
        log_data = {
            "user_agent": user_agent,
            "remote_addr": remote_addr,
            "short_code": short_code,
            "created_at": timezone.localtime(timezone.now()).strftime(DATE_TIME_FORMAT)
        }
        get_logger().error(json.dumps(log_data))
    except Exception as e:
        print("Not Logged " + e.args[0])
