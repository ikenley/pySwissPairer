import awsgi
from api import create_app

app = create_app()
# cli.register(app)


def lambda_handler(event, context):
    print(event)
    print(f'{event["httpMethod"]} {event["path"]}')
    print(event["headers"])

    return awsgi.response(app, event, context, base64_content_types={"image/png"})
