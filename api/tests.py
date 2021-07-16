
x = {'requestContext': {'elb': {'targetGroupArn': 'arn:aws:elasticloadbalancing:us-east-1:924586450630:targetgroup/swiss-pair-app-lambda-api/732920dcef688b51'}}, 'httpMethod': 'GET', 'path': '/api/status', 'queryStringParameters': {}, 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'max-age=0', 'host': 'swisspair.ikenley.com',
                                                                                                                                                                                                                                                       'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"', 'sec-ch-ua-mobile': '?0', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36', 'x-amzn-trace-id': 'Root=1-60f1f348-752459675b1bbec34181e326', 'x-forwarded-for': '73.133.219.140', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'body': '', 'isBase64Encoded': False}

httpMethod = x["httpMethod"]
print(httpMethod)

for key, value in x.items():
    print(key, value)
