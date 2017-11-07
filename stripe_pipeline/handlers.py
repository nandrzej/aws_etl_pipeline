import json
import boto3
import datetime as dt


class JSONFormatException(Exception):
    """
    Exception representing errors in input JSON
    like missing expected keys, etc.
    """


s3 = boto3.client('s3')

dynamodb = boto3.client('dynamodb')


def save_source_in_s3(event, context):
    source = validate_and_extract(event, ('data', 'object', 'source'))

    now = dt.datetime.now()
    s3.Object('stripe_payments',
              '{:%Y-%m-%d}/{}'.format(now,
                                      now.timestamp())).put(Body=source)


def put_in_dynamodb(event, context):
    payment = validate_and_extract(event, ('data', 'object'))

    dynamodb.put_item(
        Item={
            'PaymentId': {
                'S': payment['id'],
            },
            'CustomerId': {
                'S': payment['source']['customer'],
            },
            'NameOnPayment': {
                'S': payment['source']['name'],
            },
            'BillingCountry': {
                'S': payment['source']['country'],
            },
            'BillingAddress': {
                'S': '{} {}'.format(
                    payment['source']['address_line1'],
                    payment['source']['address_line2']),
            },
            'BillingCity': {
                'S': payment['source']['address_line1'],
            },
            'BillingZipCode': {
                'S': payment['source']['address_zip'],
            },
            'PaymentType': {
                'S': payment['source']['type'],
            },
            'PaymentAmount': {
                'S': payment['amount'],
            },
            'PaymentDate': {
                'S': dt.datetime.utcfromtimestamp(
                    payment['created']).isoformat(),
            },
        },
        TableName='PaymentTable',
    )


def validate_and_extract(json_string, path):
    try:
        stripe_data = json.loads(json_string)
    except (json.decoder.JSONDecodeError, TypeError) as decoding_error:
        raise JSONFormatException(
            'Decoding error encountered') from decoding_error

    return get_value(stripe_data, path)


def get_value(a_dict, keys):
    if keys[0] in a_dict:
        if len(keys) == 1:
            return a_dict[keys[0]]
        else:
            return get_value(a_dict[keys[0]], keys[1:])
    else:
        raise JSONFormatException(
            '{} not found in input JSON'.format(keys[0]))
