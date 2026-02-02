from flask import Flask, render_template, redirect, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from utils.forms import RegisterForm, LoginForm

app = Flask(__name__, template_folder="template", static_folder="static")
app.secret_key = "Niko_ikke_noe_hacke_her"


def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="ludde",
        password="123Akademiet",
        database="handleliste_db"
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        navn = form.name.data
        brukernavn = form.username.data
        passord = generate_password_hash(form.password.data)
        
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO kunder (navn, brukernavn, passord) VALUES (%s, %s, %s)",
                (navn, brukernavn, passord)
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect("/login")
        except Exception as e:
            print(f"Error during registration: {e}")
            form.username.errors.append("Brukernavn er allerede i bruk eller databasefeil")
    
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        brukernavn = form.username.data
        passord = form.password.data

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT navn, passord FROM kunder WHERE brukernavn=%s",
            (brukernavn,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[1], passord):
            session['brukernavn'] = brukernavn
            session['bruker_navn'] = user[0]
            return redirect("/handleliste")
        else:
            form.username.errors.append("Feil brukernavn eller passord")
    
    return render_template("login.html", form=form)

@app.route('/')
def index():
    return render_template('index.html', active_page='index')

@app.route('/handleliste', methods=["GET", "POST"])
def handleliste():
    innlogget = 'brukernavn' in session
    
    # Håndter login fra handleliste siden
    if request.method == "POST" and not innlogget:
        brukernavn = request.form.get('brukernavn')
        passord = request.form.get('passord')
        
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT navn, passord FROM kunder WHERE brukernavn=%s",
            (brukernavn,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user and check_password_hash(user[1], passord):
            session['brukernavn'] = brukernavn
            session['bruker_navn'] = user[0]
            return redirect("/handleliste")
        else:
            # Logg inn feilet, vis siden igjen med feilmelding
            pass
    
    return render_template('handleliste.html', active_page='handleliste', innlogget=innlogget, varer=[])

@app.route('/kategorier')
def kategorier():
    return render_template('kategorier.html', active_page='kategorier')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5001)





