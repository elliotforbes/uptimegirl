import urllib.request
import os

def lambda_handler(event, context):
    request = urllib.request.Request(os.getenv('URL', ''))
    
    try:
        urllib.request.urlopen(request)
        print()
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())
    else:
        print("{} is currently up!".format(os.getenv('URL','')))
    
    return str(request)
