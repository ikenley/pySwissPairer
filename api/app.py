import awsgi
from api import create_app

app = create_app()
# cli.register(app)


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})
