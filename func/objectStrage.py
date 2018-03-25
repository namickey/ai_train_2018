from ibm_botocore.client import Config
import ibm_boto3
cos_credentials={
  "apikey": "PzAhGo3_FzaBWfgM0MG7x6ZAodwTu3Z0NCnWZDO6y2HF",
  "endpoints": "https://cos-service.bluemix.net/endpoints",
  "iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:cloud-object-storage:global:a/7522907cacecbc549c2117b1d5ecd44f:a858574c-e891-4531-aa19-e2b21406763c::",
  "iam_apikey_name": "auto-generated-apikey-9cd9015a-66b6-4762-b9f7-53b69d1e363f",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/7522907cacecbc549c2117b1d5ecd44f::serviceid:ServiceId-236414ac-c50e-4048-959c-e9bb661d7ac6",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/7522907cacecbc549c2117b1d5ecd44f:a858574c-e891-4531-aa19-e2b21406763c::"
}

auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3.us-south.objectstorage.softlayer.net'

cos = ibm_boto3.client('s3',
                         ibm_api_key_id=cos_credentials['apikey'],
                         ibm_service_instance_id=cos_credentials['resource_instance_id'],
                         ibm_auth_endpoint=auth_endpoint,
                         config=Config(signature_version='oauth'),
                         endpoint_url=service_endpoint)

#cos.put_object(Body=b'foobar', Bucket='bag', Key='foo.txt')
for bucket in cos.list_buckets()['Buckets']:
  print(bucket['Name'])
response = cos.get_object(Bucket='bag', Key='foo.txt')
print("Done, response body:")
print(response['Body'].read())
