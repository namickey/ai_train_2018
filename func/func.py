#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import requests
import ibm_db

def adddata(name=None):
    db2cred = {
      "port": 50000,
      "db": "BLUDB",
      "username": "kvt88678",
      "ssljdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;",
      "host": "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
      "https_url": "https://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
      "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=kvt88678;PWD=5mgcq^dd69km5t2q;",
      "hostname": "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
      "jdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50000/BLUDB",
      "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=kvt88678;PWD=5mgcq^dd69km5t2q;Security=SSL;",
      "uri": "db2://kvt88678:5mgcq%5Edd69km5t2q@dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50000/BLUDB",
      "password": "5mgcq^dd69km5t2q"
    }
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        sql="select max(id) as id from sample"
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        sql="insert into sample(id, name) values(?, ?)"
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, result['ID']+1)
        ibm_db.bind_param(stmt, 2, name)
        ibm_db.execute(stmt)
        ibm_db.close(db2conn)

def main(dict):
    print(dict['img'])
    adddata(dict['img'])
    url = 'https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=befb491ae8c532e1db72518f6da8088bb2bd1b52&url=https://namickey.github.io/ai_train_2018/img/'+dict['img']+'&version=2016-05-20'
    headers = {'Accept-Language': 'ja'}
    tmpResponse = requests.get(url, headers=headers)
    return tmpResponse.json()
