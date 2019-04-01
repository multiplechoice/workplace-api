import datetime
import os
from collections import defaultdict
from itertools import chain

from flask import Flask, jsonify, request
from flask_compress import Compress
from flask_cors import CORS
from mappings import ScrapedJob
from mappings.utils import session_scope

app = Flask(__name__)
CORS(app)
Compress(app)
credentials = os.environ.get('PG_CREDS')


def flatten(lists):
    """
    Flatten one level of nesting. Courtesy of itertools recipes.

    Args:
        lists (list): a list of lists.

    Returns:
        list: list containing elements from the nested lists

    """
    return chain.from_iterable(lists)


def valid_date(date):
    """
    Does a quick check on the date to avoid doing a db dip to get an error we could have avoided

    Args:
        date (string): the date input that we're validating

    Returns:
        bool: whether or not we think the given input string is a date or not

    """
    if date is None:
        return False

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    return True


def group_results(results, key='spider'):
    """
    Groups the results by a key. If the given key is not found in the item, the item is added to
    an extra grouping at the end, titled "unknown"

    Args:
        results (list): a list of items (dicts) that we wish to group
        key (str): the key in the items to group by

    Returns:
        dict: the results grouped by the specified key

    """
    grouped_results = defaultdict(list)
    for item in results:
        if key in item:
            grouped_results[item[key]].append(item)
        else:
            grouped_results['unknown'].append(item)

    return grouped_results


class Arguments(object):
    pass


def get_args():
    """
    Extracts known arguments from the incoming request, supplying a default value and maximum clamping, where
    necessary.

    Returns:
        obj:`Arguments`: simple object containing the extracted parameters

    """
    args = Arguments()
    args.n_days = min(request.args.get('days', default=7, type=int), 31)
    args.n_results = min(request.args.get('results', default=100, type=int), 1000)
    args.group_by_spider = request.args.get('group', default=False, type=bool)
    return args


@app.route('/date/<date>')
def get_by_date_of_posting(date):
    if not valid_date(date):
        return jsonify([])

    args = get_args()
    with session_scope(credentials) as session:
        query = session.query(ScrapedJob).filter(ScrapedJob.date_of_posting == date).limit(args.n_results)
        results = [row.as_dict() for row in query.all()]
        if args.group_by_spider:
            results = group_results(results)
        return jsonify(results)


@app.route('/spider/<spider>')
def get_by_spider(spider):
    args = get_args()
    with session_scope(credentials) as session:
        query = session.query(ScrapedJob).filter(ScrapedJob.spider == spider).limit(args.n_results)
        results = [row.as_dict() for row in query.all()]
        return jsonify(results)


@app.route('/all')
def get_primary_result_set():
    args = get_args()
    # return the top n results ordered by the date of their posting
    with session_scope(credentials) as session:
        query = session.query(ScrapedJob).filter(
            ScrapedJob.date_of_posting >= datetime.datetime.today().date() - datetime.timedelta(days=args.n_days)
        )
        query = query.order_by(ScrapedJob.posted.desc()).limit(args.n_results)
        results = [row.as_dict() for row in query.all()]
        if args.group_by_spider:
            results = group_results(results)
        return jsonify(results)


if __name__ == '__main__':
    app.run()
