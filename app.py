from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:schrodinger@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)


class collection(db.Model):
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/')
def index():
    stack = collection.query.all()
    for i in stack:
        print(i.name + i.email)
    return render_template('index.html', stack=stack)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        print(name, email)
        if name == '' or email == '':
            return render_template('index.html', message='The fields cannot be blank')
        if db.session.query(collection).filter(collection.email == email).count() == 0:
            data = collection(name, email)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('index.html', message='The profile already exists')

@app.route("/delete", methods=['POST'])
def delete():
    id = request.form['id']
    scapegoat = collection.query.filter_by(id = id).first()
    db.session.delete(scapegoat)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
