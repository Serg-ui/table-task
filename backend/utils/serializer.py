from datetime import datetime


def serialize(table):
    if isinstance(table, list):
        res = []

        for row in table:
            row_data = _serialize_helper(row)
            res.append(row_data)

        return res

    return _serialize_helper(table)


def _serialize_helper(row):
    res = {}

    for attr in dir(row):
        if attr.startswith('_'):
            continue

        value = getattr(row, attr)
        if isinstance(value, (str, int)):
            res[attr] = value

        if isinstance(value, datetime):
            res[attr] = value.strftime("%Y.%m.%d")

    return res
