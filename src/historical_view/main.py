import json
import boto3

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    # event contains:
    # {
    # 'resource': '/',
    # 'path': '/', # for /test/2023-11-16: "/2023-11-16"
    # 'httpMethod': 'GET'
    # 'headers'
    # 'multiValueHeaders'
    # 'queryStringParameters'
    # 'multiValueQueryStringParameters'
    # 'pathParameters'
    print(event, context)
    path = event["path"]
    date = path.split("/")[-1]
    try:
        res_body = main(date)
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(res_body),
        }
    except Exception as e:
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "headers": {},
            "body": json.dumps({"message": str(e)}),
        }


def main(date):
    # find rows that have date starting with date
    # res = dynamodb.query(
    #     TableName="half-hour-data",
    #     KeyConditions={
    #         "date": {
    #             "AttributeValueList": [{"S": date}],
    #             "ComparisonOperator": "BEGINS_WITH",
    #         }
    #     },
    # )
    res = dynamodb.query(
        TableName="half-hour-data",
        # TODO: need to add partition key (user id) and use sort key for queries
        KeyConditionExpression="begins_with(#d, :date)",
        ExpressionAttributeValues={":date": {"S": date}},
        ExpressionAttributeNames={"#d": "date"},
    )
    # return items
    items = res["Items"]
