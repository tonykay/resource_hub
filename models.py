# from app import db

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
