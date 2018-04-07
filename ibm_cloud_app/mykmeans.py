from cloudant.client import Cloudant
from cloudant.document import Document
import requests
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from ibm_botocore.client import Config
import ibm_boto3
#https://openwhisk.ng.bluemix.net/api/v1/web/namiki%40insightech.co.jp_dev/default/loginCreateToken.json?name=kani&passwd=123
#https://openwhisk.ng.bluemix.net/api/v1/web/namiki%40insightech.co.jp_dev/default/userList.json?token=test
def crecli():
    cred = {
      "username": "3f83d72a-eb9d-4da5-ae78-3fb3c7be8d05-bluemix",
      "password": "64a41c7151d17ec97fff6ee35a460cd89e00ef061f33300103685987f0bd6f7d",
      "host": "3f83d72a-eb9d-4da5-ae78-3fb3c7be8d05-bluemix.cloudant.com",
      "port": 443,
      "url": "https://3f83d72a-eb9d-4da5-ae78-3fb3c7be8d05-bluemix:64a41c7151d17ec97fff6ee35a460cd89e00ef061f33300103685987f0bd6f7d@3f83d72a-eb9d-4da5-ae78-3fb3c7be8d05-bluemix.cloudant.com"
    }
    return Cloudant(cred['username'], cred['password'], url=cred['url'], connect=True)

def makeblob(num):
    x, y = make_blobs(n_samples=num)
    return x

def creKmeans(num, group):
    mydb = crecli()['kmeans']
    for d in makeblob(num):
        data = {'x':round(d[0], 3), 'y':round(d[1], 3), 'group':group}
        mydb.create_document(data)

def delKmeans():
    mydb = crecli()['kmeans']
    for x in mydb:
        x.delete()

def checkTokenFunc(token):
    url = 'https://openwhisk.ng.bluemix.net/api/v1/web/namiki%40insightech.co.jp_dev/default/checkToken.json?token=' + token
    return requests.get(url).json()['result']

def clusterdata(data, clnum):
    return KMeans(n_clusters=clnum).fit_predict(data)

def kmeansListDb():
    kmeans = []
    for doc in crecli()['kmeans']:
        kmeans.append([doc['x'], doc['y']])
    return kmeans

def savepng():
    data = np.array(kmeansListDb())
    pred = clusterdata(data, 3)

def cres3cos():
    cos_credentials={
  "apikey": "SRoE84GJgY37s35b8_Ombfk5H2h6c7eVRXyC_hvntgND",
  "endpoints": "https://cos-service.bluemix.net/endpoints",
  "iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:cloud-object-storage:global:a/11bef123053fda60aec82db537d2b9b4:0c7aec40-1644-4e12-bf8b-3df410c20c5a::",
  "iam_apikey_name": "auto-generated-apikey-593c7907-e82c-428a-8f60-a419498464f0",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/11bef123053fda60aec82db537d2b9b4::serviceid:ServiceId-1dc7c415-853a-47a8-a5b3-8da9df9fc793",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/11bef123053fda60aec82db537d2b9b4:0c7aec40-1644-4e12-bf8b-3df410c20c5a::"
}
    auth_endpoint = 'https://iam.bluemix.net/oidc/token'
    service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'
    cos = ibm_boto3.client('s3',
                             ibm_api_key_id=cos_credentials['apikey'],
                             ibm_service_instance_id=cos_credentials['resource_instance_id'],
                             ibm_auth_endpoint=auth_endpoint,
                             config=Config(signature_version='oauth'),
                             endpoint_url=service_endpoint)
    return cos
def saves3(filename, clnum):
    data = np.array(kmeansListDb())
    pred = clusterdata(data, clnum)
    
    cres3cos().upload_file(filename, 'kame', filename)
#creKmeans(100, 1)
#savepng()
#saves3()
