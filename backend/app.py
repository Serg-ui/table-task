from distutils.util import strtobool
from flask import Flask, jsonify, request
from db.base import session
from db.main_table import MainTable
from utils import serialize
from sqlalchemy import asc, desc

import operator

ROWS_PER_PAGE = 10
CORS_HEADER = {'Access-Control-Allow-Origin': '*'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lxmcsldkcmslkdc'


@app.route("/", methods=['GET'])
def home():
    with session() as s:
        total_count = s.query(MainTable).count()

        data = s.query(MainTable).limit(ROWS_PER_PAGE).all()
        data_json = serialize(data)

    return (jsonify({'items': data_json, 'total_pages': int(total_count / ROWS_PER_PAGE)}),
            200,
            CORS_HEADER
            )


@app.route('/api/', methods=['GET'])
def main_api():
    request_data = request.args.to_dict()
    is_sort = bool(strtobool(request_data['sort_active']))
    is_filter = bool(strtobool(request_data['filter_active']))
    page = int(request_data['current_page'])

    with session() as s:
        data = s.query(MainTable)

        if is_filter:
            data = _get_filtered_data(request_data, data)

        if is_sort:
            data = _get_sorted_data(request_data, data)

        total_count = data.count()
        data = data.limit(ROWS_PER_PAGE).offset((page - 1) * ROWS_PER_PAGE).all()
        data_json = serialize(data)

    return jsonify({'items': data_json, 'total_pages': int(total_count / ROWS_PER_PAGE)}), 200, CORS_HEADER


def _get_sorted_data(req, data):
    method = bool(strtobool(req['sort_reverse']))
    column = getattr(MainTable, req['sort_column'])

    if method:
        data = data.order_by(asc(column))
    else:
        data = data.order_by(desc(column))

    return data


def _get_filtered_data(req, data):
    column = getattr(MainTable, req['filter_column'])
    filter_operator = req['filter_operator']
    filter_value = req['filter_value']

    if filter_operator == 'like':
        data = data.filter(column.like(f'%{filter_value}%'))
        return data

    ops = {
        '>': operator.gt,
        '<': operator.lt,
        '=': operator.eq
    }

    data = data.filter(ops[filter_operator](column, filter_value))

    return data
