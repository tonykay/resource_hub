from app import db, Resource


db.create_all()
db.drop_all()
db.create_all()

#roles = [ 'Admin', 'Operator', 'Moderator', 'Pleb' ]
#
#for role in roles:
#    print (role)

dataList = [
        {'a': 1, 'name' : 'tok'},
        {'a': 1, 'name' : 'tok2'},
        {'a': 1, 'name' : 'tok3'}
        ]
for dic in dataList:
        for val in dic.values():
                    print(val)


resources = [
        { 'name': 'Ansible for DevOps', 'description': 'Classic introduction to Ansible', 
        'author': 'That Jeff Geerlinguy', 'source': 'Book' },
        { 'name': 'Mastering Ansible 4rd Edition', 'description': 'Explores the plumbing', 
        'author': 'Jeff Keating', 'source': 'Book' },
        { 'name': 'Cloud Stuff', 'description': 'Explores the plumbing', 
        'author': 'Jeff Keating', 'source': 'Book' }
        ]

for r in resources:
    print(r['name'])
#    db.session.add(Resource(r['name'], r['description'], r['author'], "web", r['source']))
#    db.session.add(Resource(name=(r.['name']), description='foo', url='null', author='That Jeff Geerlinguy',
#    source='book'))

db.session.execute(Resource.__table__.insert(), resources)
#session.commit()

#db.session.add(Resource(name='Mastering Ansible, 2nd Edition', description='foo', url='null', author='Jeff Keating',
#    source='book'))



db.session.commit()

#admin_role = Role(name='Admin')
#mod_role = Role(name='Moderator')
#user_role = Role(name='User')
#user_john = User(username='peter', role=admin_role)
#user_susan = User(username='maja', role=user_role)
#user_tony = User(username='tony', role=user_role)
#db.session.add(Role(name='foobar'))
#db.session.add(admin_role)
#db.session.add(mod_role)
#db.session.add(user_role)
#db.session.add(user_john)
#db.session.add(user_susan)
#db.session.add(user_tony)
#db.session.commit()
