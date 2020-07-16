#!/usr/bin/env python3
# preload dataset from resources

from app import db, Resource
from resources import resources

db.create_all()
db.drop_all()
db.create_all()

db.session.execute(Resource.__table__.insert(), resources)

db.session.commit()

