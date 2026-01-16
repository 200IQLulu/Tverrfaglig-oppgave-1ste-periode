from flask import Flask, render_template

app = Flask(__name__, template_folder="template", static_folder="static")

@app.route('/')
def index():
    return render_template('index.html', active_page='index')

@app.route('/handleliste')
def handleliste():
    return render_template('handleliste.html', active_page='handleliste')

@app.route('/kategorier')
def kategorier():
    return render_template('kategorier.html', active_page='kategorier')

if __name__ == '__main__':
    app.run(debug=True)




