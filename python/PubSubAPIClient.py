import grpc
import requests
import threading
import io
import pubsub_api_pb2 as pb2
import pubsub_api_pb2_grpc as pb2_grpc
import avro.schema
import avro.io
import time
import certifi
import json

semaphore = threading.Semaphore(1)

latest_replay_id = None

with open(certifi.where(), 'rb') as f:
    creds = grpc.ssl_channel_credentials(f.read())
with grpc.secure_channel('api.pubsub.salesforce.com:7443', creds) as channel:
    # All of the code in the rest of the tutorial will go inside this block.
    # Make sure that the indentation of the new code you add starts from this comment’s block.

username = '{your username}'
password = '{your password}'
url = '{the appropriate login URL}'
headers = {'content-type': 'text/xml', 'SOAPAction': 'login'}
xml = f"""<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
xmlns:urn='urn:partner.soap.sforce.com'><soapenv:Body>
<urn:login>
<urn:username><![CDATA[{username}]]></urn:username>
<urn:password><![CDATA[{password}]]></urn:password>
</urn:login></soapenv:Body></soapenv:Envelope>"""
res = requests.post(url, data=xml, headers=headers, verify=False)
#Optionally, print the content field returned
print(res.content)