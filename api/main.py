from datetime import date, timedelta
from aiohttp import web
import aiohttp_cors
import boto3
import re

app = web.Application()
cors = aiohttp_cors.setup(app)

AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
REGION='eu-west-1'

lambda_client = boto3.client('lambda', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)
cloudwatch_client = boto3.client('cloudwatch', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)
cloudwatch_events_client = boto3.client('events', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

async def get_functions(request):
    functions = lambda_client.list_functions()
    return web.json_response(functions)


async def create_lambda_function(request):
    env = dict()
    env['Variables'] = dict()
    env['Variables']['URL'] = request.rel_url.query['url']

    func_name = re.sub(r'\W+', '', request.rel_url.query['url'])

    code = dict()
    code['ZipFile'] = open('lambda.zip', 'rb').read()
    try:
        response = lambda_client.create_function(FunctionName=func_name, Runtime='python3.6', Role='arn:aws:iam::853957954650:role/service-role/testLambda', 
            Handler='lambda_function.lambda_handler', Code=code, Environment=env)

        print(response)

        target = dict()
        curr_rules = cloudwatch_events_client.list_targets_by_rule(Rule='15-min')
        target['Id'] = str(len(curr_rules['Targets']) + 1)
        target['Arn'] = str(response['FunctionArn'])
        cloudwatch_events_client.put_targets(Rule='15-min', Targets=[target])
        return web.Response(text=str("Successfully created function and attached rule"))
    except Exception as e:
        print(e)
        return web.Response(text=str(e))


app.router.add_get('/funcs', get_functions)
app.router.add_get('/create', create_lambda_function)

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

for route in list(app.router.routes()):
    cors.add(route)

if __name__ == '__main__':
    web.run_app(app)