from collections import OrderedDict

from utilities.code_texts import CODES_TEXTS


def response_formatter(http_code, data=None, errors=None, non_field_errors=None):
    """
    Custom response formatter
    :param http_code:
    :param data:
    :param errors:
    :param non_field_errors:
    :return:
    """
    return_info_dict = OrderedDict()

    if http_code in CODES_TEXTS.keys():
        return_info_dict["code"] = http_code
        return_info_dict["message"] = CODES_TEXTS[http_code]

        if data is not None:
            return_info_dict["data"] = data

        if errors:
            return_info_dict["errors"] = OrderedDict()
            return_info_dict["errors"] = errors

        if non_field_errors is not None:
            return_info_dict["non_field_errors"] = OrderedDict()
            return_info_dict["non_field_errors"] = non_field_errors

        return return_info_dict

    return {"code": 5000, "text": CODES_TEXTS[5000]}
