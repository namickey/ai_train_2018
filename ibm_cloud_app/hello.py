from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import cf_deployment_tracker
import json
import requests
import ibm_db
import galpy

# Emit Bluemix deployment event
cf_deployment_tracker.track()
# must needed by Bluemix setting
port = int(os.getenv('PORT', 8000))

app = Flask(__name__)

@app.route('/km', methods=['GET'])
def km():
    return '<html><body>%s</body></html>' % galpy.pygal_stat()

@app.route('/vreco/<img>', methods=['GET'])
def visualReco(img):
    adddata(img)
    # call visual-recognition webapi
    url = 'https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=befb491ae8c532e1db72518f6da8088bb2bd1b52&url=https://namickey.github.io/ai_train_2018/img/'+img+'&version=2016-05-20'
    headers = {'Accept-Language': 'ja'}
    tmpResponse = requests.get(url, headers=headers)

    # allow-origin
    newJsonResponse = jsonify(tmpResponse.json())
    newJsonResponse.headers.add('Access-Control-Allow-Origin', '*')
    return newJsonResponse

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
