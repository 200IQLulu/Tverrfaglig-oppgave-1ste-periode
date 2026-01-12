from flask import Flask, render_template, request, redirect
from handleliste import legg_til_vare, hent_liste
form lagring import last_liste, lagre_liste

app = Flask(__name__)

handleliste = last_liste()

@app.route('/', methods=['GET', 'POST'])
