from flask import Flask, render_template

app = Flask(__name__, template_folder="template", static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handleliste')
def handleliste():
    return render_template('handleliste.html')

@app.route('/kategorier')
def kategorier():
    return render_template('kategorier.html')

if __name__ == '__main__':
    app.run(debug=True)
