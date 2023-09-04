import re


def get_integrity_violation_key_name(orig_arg: str) -> str:
    """
    function which extracts name of the table key which caused
    IntegrityError; as an input receives exception arg
    :param orig_arg: exception's arg
    :return: str; value
    """
    detail = orig_arg.split("Key")
    key = re.split(r"[()=]", detail[1])[1]
    return key
