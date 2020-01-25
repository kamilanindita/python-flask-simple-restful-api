from flask import Flask,render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_DB"]="website_crud"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)

app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def index():
    title="Index"
    return render_template("index.html",title=title)
    
@app.route("/buku",methods=["GET","POST"])
def buku():
    if request.method=="GET" :
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM buku")
        data = cur.fetchall()
        cur.close()

        if data :
            return jsonify({'status':'success', 'message':'Data found', 'data': data })
        else:
            return jsonify({'status':'failed', 'message':'Data not found', 'data': [] })


    elif request.method=="POST" :
        penulis=request.form["penulis"]
        judul=request.form["judul"]
        kota=request.form["kota"]
        penerbit=request.form["penerbit"]
        tahun=request.form["tahun"]
        
        data=(penulis,judul,kota,penerbit,tahun)
        query="INSERT INTO buku (penulis,judul,kota,penerbit,tahun) VALUES (%s,%s,%s,%s,%s)"
        cur = mysql.connection.cursor()
        result=cur.execute(query,data)
        mysql.connection.commit()
        cur.close()
        
        if result > 0 :
            return jsonify({'status':'success', 'message':'Data has been created', 'data': [] })
        else:
            return jsonify({'status':'failed', 'message':'Data not created', 'data': [] })

    
    else :
        return "Error method is not allowed"



@app.route("/buku/<int:id>",methods=["GET", "PUT", "DELETE"])
def bukuBy(id):
    if request.method=="GET" :
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM buku WHERE id={}".format(id))
        data = cur.fetchone()
        cur.close()

        if data :
            return jsonify({'status':'success', 'message':'Data found', 'data': data })
        else:
            return jsonify({'status':'failed', 'message':'Data not found', 'data': [] })


    elif request.method=="PUT" :
        penulis=request.form["penulis"]
        judul=request.form["judul"]
        kota=request.form["kota"]
        penerbit=request.form["penerbit"]
        tahun=request.form["tahun"]
        
        data_update=(penulis,judul,kota,penerbit,tahun)
        query="UPDATE buku SET penulis = %s, judul = %s, kota = %s, penerbit = %s, tahun = %s WHERE id = {}".format(id)
        cur = mysql.connection.cursor()
        result=cur.execute(query,data_update)
        mysql.connection.commit()
        cur.close()

        if result > 0 :
            return jsonify({'status':'success', 'message':'Data has been updated', 'data': [] })
        else:
            return jsonify({'status':'failed', 'message':'Data not updated', 'data': [] })


    elif request.method=="DELETE" :
        query="DELETE FROM buku WHERE id={}".format(id)
        cur = mysql.connection.cursor()
        result=cur.execute(query)
        mysql.connection.commit()
        cur.close()
        
        if result > 0:
            return jsonify({'status':'success', 'message':'Data has been deleted', 'data': [] })
        
        else:
            return jsonify({'status':'failed', 'message':'Data not deleted', 'data': [] })

    else :
        return "Error method is not allowed"
    
if __name__ == '__main__':
    app.run(debug=True)
