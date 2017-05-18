import json
from cStringIO import StringIO

import boto3
from flask import Flask, jsonify

app = Flask(__name__)
s3 = boto3.client('s3')
bucket = 'lambda-multiplechoice-workplace'
folder = 'scrapinghub/'


def get_list_of_s3_objects(path):
    objects = s3.list_objects_v2(Bucket=bucket, Prefix=path)
    return objects.get('Contents')


def get_contents_of_s3_object(path):
    # gets the contents of the s3 object and decodes the json inside it. if it doesn't contain json
    # it will explode
    file_like_object = StringIO()
    s3.download_fileobj(bucket, path, file_like_object)
    payload = json.loads(file_like_object.getvalue())
    return payload


def get_common_prefixes_of_s3_objects(path):
    # the results from the spiders get uploaded with paths like 'scrapinghub/visir_2017-05-17T19-41-53.json'
    # meaning we can use a prefix of 'scrapinghub/' and a delimiter of '_' to group the files into the
    # various spiders, removing the need to maintain a list of spiders we support
    objects = s3.list_objects_v2(Bucket=bucket, Prefix=path, Delimiter='_')
    return objects.get('CommonPrefixes')


def get_most_recently_modified_object(objects):
    # sorts the list of objects by their last modified key, taking the most recently modified as the
    # latest and returning it's path
    latest = sorted(objects, key=lambda x: x['LastModified'], reverse=True)[0]
    return latest['Key']


@app.route('/spider/<spider>')
def get_spider_results(spider):
    objects = get_list_of_s3_objects(folder + spider)
    if objects is None:
        return jsonify({})

    latest = get_most_recently_modified_object(objects)
    payload = get_contents_of_s3_object(latest)
    return jsonify(payload)


@app.route('/all')
def get_all_results():
    common_prefixes = get_common_prefixes_of_s3_objects(folder)
    if common_prefixes is None:
        return jsonify({})

    payload = []
    for prefix in common_prefixes:
        matching_prefix = prefix['Prefix']
        objects = get_list_of_s3_objects(matching_prefix)
        latest = get_most_recently_modified_object(objects)
        payload.extend(get_contents_of_s3_object(latest))

    return jsonify(payload)


if __name__ == '__main__':
    app.run()
