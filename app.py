import datetime
from itertools import chain

from flask import Flask, jsonify
from flask_compress import Compress
from flask_cors import CORS
from mappings import ScrapedJob
from mappings.utils import session_scope
from sqlalchemy import func, cast
from sqlalchemy.dialects.postgresql import DATE

app = Flask(__name__)
CORS(app)
Compress(app)
credentials = 'postgresql://alexander@localhost:5432/alexander'


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
        date (basestring): the date input that we're validating

    Returns:
        bool: whether or not we think the given input string is a date or not

    """
    if not isinstance(date, basestring):
        return False

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    return True


@app.route('/date/<date>')
def get_all_results(date):
    if not valid_date(date):
        return jsonify([])

    with session_scope(credentials) as session:
        query = session.query(ScrapedJob.data).filter(
            cast(func.date_trunc('day', ScrapedJob.posted), DATE) == date
        )
        return jsonify(list(flatten(query.all())))


if __name__ == '__main__':
    app.run()
