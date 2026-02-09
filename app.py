# Importerer nødvendige biblioteker for Flask-applikasjonen
from flask import Flask, render_template, redirect, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from utils.forms import RegisterForm, LoginForm, VareForm

# Initialiserer Flask-applikasjonen med template- og static-mapper
app = Flask(__name__, template_folder="template", static_folder="static")
app.secret_key = "Niko_ikke_noe_hacke_her"


def get_conn():
    """
    Oppretter og returnerer en ny tilkobling til MySQL-databasen.
    Brukes av alle ruter som trenger å få tilgang til data.
    """
    return mysql.connector.connect(
        host="localhost",
        user="ludde",
        password="123Akademiet",
        database="handleliste_db"
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Håndterer brukerregistrering.
    - GET: Viser registreringsskjemaet
    - POST: Registrerer ny bruker med navn, brukernavn og kryptert passord
    """
    form = RegisterForm()
    if form.validate_on_submit():
        navn = form.name.data
        brukernavn = form.username.data
        # Krypterer passordet før det lagres i databasen
        passord = generate_password_hash(form.password.data)
        
        try:
            # Lagrer brukerdata i databasen
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO kunder (navn, brukernavn, passord) VALUES (%s, %s, %s)",
                (navn, brukernavn, passord)
            )
            conn.commit()
            cur.close()
            conn.close()
            session['brukernavn'] = brukernavn
            session['bruker_navn'] = navn
            return redirect("/handleliste")

        except Exception as e:
            # Håndterer feil, f.eks. hvis brukernavn allerede eksisterer
            print(f"Error during registration: {e}")
            form.username.errors.append("Brukernavn er allerede i bruk eller databasefeil")
    
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Håndterer brukerinnlogging.
    - GET: Viser innloggingsskjemaet
    - POST: Validerer brukernavn og passord, og setter sesjonsvariabler hvis vellykket
    """
    form = LoginForm()
    if form.validate_on_submit():
        brukernavn = form.username.data
        passord = form.password.data

        # Henter brukerdata fra databasen
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT navn, passord FROM kunder WHERE brukernavn=%s",
            (brukernavn,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        # Sjekker om brukernavn finnes og passordet er korrekt
        if user and check_password_hash(user[1], passord):
            # Lagrer brukerinformasjon i sesjonen
            session['brukernavn'] = brukernavn
            session['bruker_navn'] = user[0]
            return redirect("/handleliste")
        else:
            form.username.errors.append("Feil brukernavn eller passord")
    
    return render_template("login.html", form=form)

@app.route('/')
def index():
    """Viser startside"""
    return render_template('index.html', active_page='index')

@app.route('/handleliste', methods=["GET", "POST"])
def handleliste():
    """
    Håndterer handleliste-siden.
    Sjekker om bruker er innlogget, og lar innloggede brukere håndtere handlelistevarer.
    """
    # Sjekker om brukernavn finnes i sesjonen (bruker er innlogget)
    innlogget = 'brukernavn' in session
    
    # Håndter login fra handleliste siden hvis bruker ikke er innlogget
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
    
    varer = []
    if innlogget:
        # Henter varer for innlogget bruker fra databasen
        try:
            conn = get_conn()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id, vare FROM handlelistvarer WHERE brukernavn=%s ORDER BY id DESC",
                (session['brukernavn'],)
            )
            varer = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching items: {e}")
            varer = []
    
    return render_template('handleliste.html', active_page='handleliste', innlogget=innlogget, varer=varer)


@app.route('/add_vare', methods=["POST"])
def add_vare():
    """
    Legger til ny vare på handlelisten for innlogget bruker.
    """
    # Sjekker om bruker er innlogget
    if 'brukernavn' not in session:
        return redirect("/handleliste")
    
    vare = request.form.get('vare')
    
    if vare:
        try:
            # Lagrer varen i databasen
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO handlelistvarer (brukernavn, vare) VALUES (%s, %s)",
                (session['brukernavn'], vare)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error adding item: {e}")
    
    return redirect("/handleliste")

@app.route("/slett_varer", methods=["POST"])
def slett_varer():
    if 'brukernavn' not in session:
        return redirect("/handleliste")

    ids = request.form.getlist("slett_ids")  # henter alle avkryssede

    if not ids:
        return redirect("/handleliste")

    try:
        conn = get_conn()
        cur = conn.cursor()

        # Slett bare varer som tilhører brukeren (viktig!)
        for vare_id in ids:
            cur.execute(
                "DELETE FROM handlelistvarer WHERE id=%s AND brukernavn=%s",
                (vare_id, session['brukernavn'])
            )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error deleting items: {e}")

    return redirect("/handleliste")

@app.route('/slett_bruker', methods=["POST"])
def slett_bruker():
    # Sjekk om noen er innlogget
    if 'brukernavn' not in session:
        return redirect('/login')

    brukernavn = session['brukernavn']

    try:
        conn = get_conn()
        cur = conn.cursor()
        # Slett brukeren fra kundetabellen
        cur.execute("DELETE FROM kunder WHERE brukernavn=%s", (brukernavn,))
        # Slett alle varer tilknyttet brukeren
        cur.execute("DELETE FROM handlelistvarer WHERE brukernavn=%s", (brukernavn,))
        conn.commit()
        cur.close()
        conn.close()
        # Tøm sesjonen
        session.clear()
    except Exception as e:
        print(f"Error deleting user: {e}")

    return redirect('/')


@app.route('/kategorier')
def kategorier():
    """Viser kategori-siden"""
    return render_template('kategorier.html', active_page='kategorier')

@app.route('/logout')
def logout():
    """Logger ut brukeren ved å slette alle sesjonsvariabler"""
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)