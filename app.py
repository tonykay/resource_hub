

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
    'postgresql://flask:redhat@database-01:5432/flask_db'

    # 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

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

# Resouces view functions (HTML and API)
@app.route('/resources')
@app.route('/resources.html')
def get_all():
    try:
        resources = Resource.query.all()
        return render_template('resources.html', site=site, resources=resources)
    except Exception as e:
        return(str(e))  

@app.route('/api/v1/resources')
@app.route('/api/resources')
def api_get_all():
    try:
        resources = Resource.query.all()
        return  jsonify([e.serialize() for e in resources])
    except Exception as e:
        return(str(e))

# Housekeeping view functions

@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html', site=site)

@app.route('/ansible_docs')
@app.route('/ansible_docs.html')
def ansible_docs():
    return render_template('ansible_docs.html', site=site)

@app.route('/ping')
@app.route('/ping.html')
def ping():
    return render_template('ping.html', site=site)

@app.route('/cheatsheets')
@app.route('/cheatsheets.html')
def cheatsheets():
    return render_template('cheatsheets.html', site=site)

@app.route('/resources_api')
@app.route('/resources_api.html')
def resources_api():
    return render_template('resources_api.html', site=site)

@app.errorhandler(404)                  # Simple 404 Error handler
def page_not_found(e):
    return render_template('404.html', site=site), 404

@app.errorhandler(500)                  # Simple 500 Server error
def internal_server_error(e):
    return render_templatYe('500.html', site=site), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')    
