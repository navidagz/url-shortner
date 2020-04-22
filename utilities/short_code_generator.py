import base64
import re
from uuid import uuid4

from url_shortener.settings import RETRY_THRESHOLD, SHORT_CODE_MIN_LENGTH, SHORT_CODE_MAX_LENGTH


def code_generator(size=SHORT_CODE_MIN_LENGTH):
    """
    Short code generator function
    :param size:
    :return:
    """
    # Generate url save base64 encoded string without some characters (-, =, _)
    return re.sub('\ |-|_|=', '', base64.urlsafe_b64encode(uuid4().bytes).strip(b"=").decode())[:size]


def create_short_code(instance, size=SHORT_CODE_MIN_LENGTH, retries=0):
    """
    Create short code
    :param instance:
    :param size:
    :param retries:
    :return:
    """

    # If retries passed specific threshold then increase the size
    if retries > RETRY_THRESHOLD:
        size += 1

    short_code = code_generator(size=size)

    # Check for code existence in database
    qs_exists = instance.objects.filter(short_code=short_code).exists()
    if qs_exists:
        # If did exists then increase the retries and create another code
        retries += 1
        return create_short_code(instance, size=size, retries=retries)

    # Return code
    return short_code


def suggested_short_code_validator(instance, short_code, retries=0):
    """
    Handle suggested short code validator
    :param instance:
    :param short_code:
    :param retries:
    :return:
    """

    # If retries passed specific threshold then create short code without taking account of suggested code
    if retries > RETRY_THRESHOLD:
        return create_short_code(instance)

    # Replace suggested code's some characters to make it more comprehensive
    short_code = re.sub('\ |-|_|=', '', short_code)

    # If retries passed zero then add some random characters to the end of it to make it more like suggested code
    if retries > 0:
        short_code = short_code + "-" + code_generator()[:SHORT_CODE_MAX_LENGTH - len(short_code) - 1]

    # Check for code existence in database
    qs_exists = instance.objects.filter(short_code=short_code).exists()
    if qs_exists:
        # If did exists then increase the retries and create another code
        retries += 1
        return suggested_short_code_validator(instance, short_code, retries=retries)

    # Return code
    return short_code
