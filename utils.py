import time
from datetime import datetime
from typing import List, Tuple


class ProcessException(Exception):
    """Exception related to mistakes from users."""


def process_text(text: str) -> List[Tuple[float, str]]:
    list_of_items = text.split('\n')
    list_of_items.pop(0)

    list_of_items = list(map(lambda i: i.split('-'), list_of_items))
    try:
        list_of_items = [(float(q), i) for q, i in list_of_items]
    except ValueError as e:
        raise ProcessException("User sent a wrong value for quantite. %s" % e)

    return list_of_items


class Converters:

    @staticmethod
    def timestamp2datetime(timestamp) -> str:
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")

    @staticmethod
    def datetime2timestamp(datetime) -> float:
        return time.mktime(datetime.timetuple())
