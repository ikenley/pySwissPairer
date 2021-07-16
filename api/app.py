import awsgi
from api import create_app

app = create_app()
# cli.register(app)


def lambda_handler(event, context):
    headers = event["headers"]
    requestData = {
        "httpMethod": event["httpMethod"],
        "path": event["path"],
        "queryStringParameters": event["queryStringParameters"],
        "headers": {
            "host": headers["host"],
            "user-agent": headers["user-agent"],
            "x-amzn-trace-id": headers["x-amzn-trace-id"],
            "x-forwarded-for": headers["x-forwarded-for"],
            "x-forwarded-proto": headers["x-forwarded-proto"]
        }
    }
    print(requestData)

    return awsgi.response(app, event, context, base64_content_types={"image/png"})
