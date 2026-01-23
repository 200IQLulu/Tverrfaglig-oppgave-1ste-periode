from flask import Flask, render_template, session
import mysql.connector

app = Flask(__name__, template_folder="template", static_folder="static")
app.secret_key = "hemmelig-nok"

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="ludde",
        password="123Akademiet",
        database="handleliste_db"
    )

@app.route('/')
def index():
    conn = get_conn()
    cur = conn.cursor() 
    cur.execute(
    "INSERT INTO brukere (bruker, passord) VALUES (%s, %s)",
    ('ludde', 'heihei')
    )
    conn.commit()
    
    return render_template('index.html', active_page='index')

@app.route('/handleliste')
def handleliste():
    return render_template('handleliste.html', active_page='handleliste')

@app.route('/kategorier')
def kategorier():
    return render_template('kategorier.html', active_page='kategorier')

if __name__ == '__main__':
    app.run(debug=True, port=5001)




