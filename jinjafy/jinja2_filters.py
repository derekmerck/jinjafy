from datetime import datetime
import logging
from pprint import pformat


def j2_bystart(items, reverse=False):
    items.sort(key=lambda k: k['startdate'] or k['enddate'], reverse=reverse)
    return items


def j2_sortcsl(keys, bibliography, reverse=False):

    dates = []
    for key in keys:
        item = [x for x in bibliography["references"] if x["id"] == key][0]
        date_kwargs = item.get("issued")[0]

        # logging.debug(pformat(date_kwargs))

        dates.append( datetime(
            year=date_kwargs.get("year"),
            month=date_kwargs.get("month", 1),
            day=date_kwargs.get("day", 1) ) )

    result = [key for _, key in sorted(zip(dates, keys))]

    if reverse:
        result = reversed(result)

    return result

