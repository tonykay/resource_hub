

import os
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# TODO: Remove basedir once switched to postgres etc
basedir = os.path.abspath(os.path.dirname(__file__))
site = { 'title' : "N Tier Flask App" } # My additions for Title, simplify passing metadata

app = Flask(__name__)
bootstrap = Bootstrap(app)              # Setting up bootstrap

# app.config.from_object(os.environ['APP_SETTINGS'])

app.config['SECRET_KEY'] = 'r3dh4t1!'   # For now, externalize later

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TODO: abstract into ext.py and avoid circular dependencies

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(256))
    url = db.Column(db.String(256))
    author = db.Column(db.String(128))
    source = db.Column(db.String(128))

    def __init__(self, name, description, url, author, source):
        self.name = name
        self.description = description
        self.url = url
        self.author = author
        self.source = source

    def __repr__(self):
        return '<Resource %r>' % self.name

    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'url': self.url,
                'author': self.author,
                'source': self.source
        }

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Resource=Resource)

# Static view functions

@app.route('/')                         # Basic view function
@app.route('/index.html')
def index():
    return render_template('index.html', site=site)
    
# API view functions 

@app.route('/api/v1/ping')
def api_ping():
    return jsonify('{ ping: "alive" }')

@app.route('/api/v1/users')
def api_get_all():
    try:
        users = User.query.all()
        # return render_template('get_all.html', site=site)
        return  jsonify([e.serialize() for e in users])
    except Exception as e:
        return(str(e))

# Housekeeping view functions


@app.route('/ping')
def ping():
    return render_template('ping.html', site=site)

@app.errorhandler(404)                  # Simple 404 Error handler
def page_not_found(e):
    return render_template('404.html', site=site), 404

@app.errorhandler(500)                  # Simple 500 Server error
def internal_server_error(e):
    return render_templatYe('500.html', site=site), 500

if __name__ == '__main__':
    app.run(debug=True)    