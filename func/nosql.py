from cloudant.client import Cloudant
from cloudant.document import Document
import datetime
import hashlib
from time import sleep
import requests
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

def creUser(name):
    mydb = crecli()['user']
    data = {'_id':name, 'pass':'123'}
    mydb.create_document(data)

def checkuser(name, passwd):
    userdb = crecli()['user']
    userdoc = Document(userdb, name)
    if userdoc.exists() and userdb[name]['pass'] == passwd:
        return True
    return False

def loginCreateToken(name, passwd):
    if not checkuser(name, passwd):
        return None
    tokendb = crecli()['token']
    nowstr = str(datetime.datetime.now())
    token = hashlib.sha256(name + nowstr).hexdigest()
    data = {'_id':token, 'name':name, 'time':nowstr.split('.')[0]}
    tokendb.create_document(data)
    return token

def checkToken(token):
    if token == 'test':
        return 'test'
    if token == None:
        return None
    tokendb = crecli()['token']
    tokendoc = Document(tokendb, token)
    if not tokendoc.exists():
        return None
    if tokendb[token]['time'] > str(datetime.datetime.now() - datetime.timedelta(seconds=7)).split('.')[0]:
        tokendoc = tokendb[token]
        tokendoc['time'] = str(datetime.datetime.now()).split('.')[0]
        tokendoc.save()
        return tokendoc['name']
    else:
        return None

def testToken():
    token = loginCreateToken('kani', '123')
    print token
    sleep(2)
    print 'sleep 2'
    print checkToken(token)

def checkTokenFunc(token):
    url = 'https://openwhisk.ng.bluemix.net/api/v1/web/namiki%40insightech.co.jp_dev/default/checkToken.json?token=' + token
    return requests.get(url).json()['result']

def userList():
    users = []
    for doc in crecli()['user']:
        users.append(doc['_id'])
    return {'users':users}
        #doc.delete()
def main():
    if checkTokenFunc(token) == None:
        return {'result':'token error'}
#creUser('kani')
#testToken()
print userList('test')
