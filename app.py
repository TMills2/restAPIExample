from flask import Flask, request, jsonify
import pyodbc
def connect():
    server = 'example12023.database.windows.net'
    database = 'example1'
    username = 'TPhil2'
    password = '{@Example1}'   
    driver= '{ODBC Driver 18 for SQL Server}'
    conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 
    cursor = conn.cursor()
    return conn
def disconnect(conn,cursor):
    cursor.close()
    conn.close()
app = Flask(__name__)

@app.route('/ex1',methods=['GET'])
def ex1Get():
    conn=connect()
    cursor=conn.cursor()
    id = request.args.get('id')
    cursor.execute('Select * from [example1].[dbo].[Example] where id= \''+id+'\';')
    row = cursor.fetchone()
    disconnect(conn,cursor)
    return jsonify(fname=row[1],
                   lname=row[2])
@app.route('/ex1',methods=['POST'])
def ex1Post():
    conn=connect()
    cursor=conn.cursor()
    id = request.args.get('id')
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    cursor.execute('Insert into [example1].[dbo].[Example] (id,fname,lname) Values '
                   +'('+ str(id) +',\''
                    + fname +'\',\''
                    + lname+'\')'+';')
    cursor.commit()
    disconnect(conn,cursor)
    return jsonify(action="success")
@app.route('/ex1',methods=['PUT'])
def ex1Put():
    conn=connect()
    cursor=conn.cursor()
    id = request.args.get('id')
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    cursor.execute('Update [example1].[dbo].[Example] SET fname =\''+fname+'\',lname =\''+lname+'\' where id ='+'\''+str(id)+'\'')
    cursor.commit()
    disconnect(conn,cursor)
    return jsonify(response="fname and lname changed")
@app.route('/ex1',methods=['Delete'])
def ex1Delete():
    conn=connect()
    cursor=conn.cursor()
    id = request.args.get('id')
    cursor.execute("delete from [example1].[dbo].[Example] where id ="+str(id))
    disconnect(conn,cursor)
    return jsonify(response="delete from ex1")

@app.route('/ex2',methods=['GET','POST','PUT','DELETE'])
def ex2():
    if request.method =='GET' :
        return jsonify(response="get from ex2")
    elif request.method =='POST' :
        return jsonify(response="post from ex2")
    elif request.method == 'PUT':
        return jsonify(response="put from ex2")
    else:
        return jsonify(response="delete from ex2")

@app.get('/ex3')
def ex3Get():
    return jsonify(response="get from ex3")
@app.post('/ex3')
def ex3Post():
    return jsonify(response="post from ex3")
@app.put('/ex3')
def ex3Put():
    return jsonify(response="put from ex3")
@app.delete('/ex3')
def ex3Delete():
    return jsonify(response="delete from ex3")

if __name__ == '__main__':
   app.run()