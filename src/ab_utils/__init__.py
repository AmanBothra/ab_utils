"""
=======
Helpers
=======
Useful helper methods that frequently used in this project
"""
import collections
from datetime import datetime, timedelta
import ntpath
import re
import os
import uuid
import pytz
import random
import string
import time
import base64
import json

first_cap_re = re.compile("(.)([A-Z][a-z]+)")
all_cap_re = re.compile("([a-z0-9])([A-Z])")


def str2bool(v):
    """
    Converts string to bool. True for any term from "yes", "true", "t", "1"
    :param str v: Term
    :return bool:
    """
    try:
        return v.lower() in ("yes", "true", "t", "1")
    except:
        return False


def string_validation(key):
    """
    Validate string does not contain any special characters
    """
    regex = re.compile("[@!#$%^&*()<>?/\|}{~:]")

    if regex.search(key):
        return False

    return True


def prop2pair(cls, out="tuple", startswith_only=None):
    """
    Iterates over each property of the cls and prepare the key-value pair
    :param cls: Class to be interated over
    :param str out: Output format either `tuple` or `dict`
    :param str startswith_only: Consider only properties that starts with this value
    :return tuple,dict:
    """
    if startswith_only is not None:
        d = {
            getattr(cls, prop)[0]: getattr(cls, prop)[1]
            if getattr(cls, prop)[1]
            else getattr(cls, prop)[0]
            for prop in dir(cls)
            if prop.startswith(startswith_only) is True
        }
    else:
        d = {
            getattr(cls, prop)[0]: getattr(cls, prop)[1]
            if getattr(cls, prop)[1]
            else getattr(cls, prop)[0]
            for prop in dir(cls)
            if prop.startswith("_") is False
        }

    if out == "tuple":
        d = list(d.items())
        # Keep tuple consistent so when migration runs it won't detect its changes
        d.sort(key=lambda x: x[0])
    elif out == "list":
        return sorted(list(d.keys()))

    return d


def round_off(value, digits=2):
    """
    Rounding off the value
    :param float value: Value to be rounded
    :param digits: Digit to kept as after point
    :return float: Rounded value
    """
    return float(("{0:.%sf}" % digits).format(value))


def camel_to_snake_case(name):
    """
    Converts given camel cased string to snake case
    For eg:
        - CamelCamelCase -> camel_camel_case
        - Camel2Camel2Case -> camel2_camel2_case
        - get2HTTPResponseCode -> get2_http_response_code
    :param str name: String to be converted
    :return str: Converted string
    """
    s1 = first_cap_re.sub(r"\1_\2", name)
    return all_cap_re.sub(r"\1_\2", s1).lower().replace(" ", "_")


def convert_into_dictionary(data):
    return json.loads(json.dumps(data))


def snake_case_to_title(s):
    """
    Converts snake case string to title case
    :param str s: String to be converted
    :return str: Converted string
    """
    return s.replace("_", " ").title().replace(" ", "")


def strip_dict(d):
    return {k: v.strip() if isinstance(v, str) else v for k, v in d.items()}


def utc_to_local_time(t, to_tz, fmt="%H:%M"):
    utc_tz = pytz.timezone("UTC")
    local_tz = pytz.timezone(to_tz)

    dt = datetime.datetime.combine(datetime.date.today(), t)
    local_dt = utc_tz.localize(dt).astimezone(local_tz)
    if fmt is None:
        return local_dt.time()
    return local_dt.strftime(fmt)


def path_leaf(path):
    """
    Extracts file name from given path
    :param str path: Path be extracted the file name from
    :return str: File name
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def flatten_dict(d, parent_key="", sep="."):
    items = []

    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


def get_proper_file_name(file_name, extension):
    """
    Removes special charcter from filename
    """
    return re.sub("[^A-z0-9 -]", "", file_name) + f".{extension}"


def app_urlname(value, arg, user=None):
    """Given model opts (model._meta) and a url name, return a named pattern.
    URLs should be named as: customadmin:app_label:model_name-list"""

    pattern = "%s:%s-%s" % (value.app_label, value.model_name, arg)
    return pattern


def get_upload_to_uuid(self, filename):
    """Rename uploaded file to a unique name."""
    basename = os.path.basename(filename)
    ext = os.path.splitext(basename)[1].lower()
    new_name = uuid.uuid4().hex
    return os.path.join(self.upload_to, new_name + ext)


def increment_date_time(value):
    now = datetime.now()
    now_plus = now + timedelta(minutes=value)
    return now_plus


def get_today_date():
    return datetime.date.today()


def get_now():
    return datetime.now().time()


def random_generator_code(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for x in range(size))


def random_digit_generator(size=6, chars=string.digits):
    return "".join(random.choice(chars) for x in range(size))


def random_string():
    string = datetime.now()
    return string.strftime("%Y" "%m" "%d" "%H" "%M" "%S" "%m") + str(
        random.randint(1000, 9999)
    )


def get_current_mili_time():
    return int(round(time.time() * 1000))


def get_last_milli_time(value):
    return round(value.timestamp() * 1000)


def datetimeToStringDateTime(date, format):
    return date.strftime(format)


def merge_dict(dict1, dict2):
    "Merge dictionaries and keep values of common keys in list"
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value, dict1[key]]
    return dict3


def decode_base64(data, altchars=b"+/"):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb"[^a-zA-Z0-9%s]+" % altchars, b"", data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b"=" * (4 - missing_padding)
    return base64.b64decode(data, altchars)


def base64_to_content(base64_content):
    """
    @params: content (large text) : content of bash64
        example: "data:audio/ogg;base64,T2dnUwACAAAAAAAAAAC7sXrhAAAAA"

    @return: file with file type
    """
    try:
        content = base64_content.split(",")[1]
        base64_decode = decode_base64(bytes(content, "utf-8"))
    except Exception:
        base64_decode = "No base64 code"

    return base64_decode


def smart_truncate(content, length=15, suffix="..."):
    if len(content) <= length:
        return content
    else:
        return " ".join(content[: length + 1].split(" ")[0:-1]) + suffix


def check_date_format(date):
    if "-" in date:
        try:
            return datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return datetime.strptime(date, "%d-%m-%Y")
        except Exception:
            return False
    elif "/" in date:
        try:
            return datetime.strptime(date, "%Y/%m/%d")
        except ValueError:
            return datetime.strptime(date, "%d/%m/%Y")
        except Exception:
            return False
    else:
        return False
