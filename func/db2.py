import ibm_db

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

def adddata(db2cred, name=None):
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        sql="select max(id) as id from sample"
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        print result
        print result['ID']+1
        sql="insert into sample(id, name) values(?, ?)"
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, result['ID']+1)
        ibm_db.bind_param(stmt, 2, name)
        ibm_db.execute(stmt)
        ibm_db.close(db2conn)

def getall(db2cred):
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        sql="select * from sample"
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            aa = result.copy()
            rows.append(aa)
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
        return rows

def getdata(db2cred, name=None):
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        sql="select * from sample where name=?"
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            aa = result.copy()
            rows.append(aa)
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
        return rows
#adddata(db2cred, 'bb')
for x in getall(db2cred):
    print x
