from app import db, app
from app.models import User, BlogType, BlogPost

app_context = app.app_context()
app_context.push()

#db.engine.execute("DROP TABLE BlogType CASCADE")

db.drop_all()
db.create_all()


u1 = User(id=1,username='John', email='1@gmail.com')
u2 = User(id=2,username='Mary', email='2@gmail.com')
u1.set_password("1")
u2.set_password("2")
db.session.add_all([u1,u2])


type1 = BlogType(id=1,type='Travel')
type2 = BlogType(id=2,type='Food')
type3 = BlogType(id=3,type='Pet')
db.session.add_all([type1,type2,type3])


bp1 = BlogPost(id=1,title='JP',description='good',blogtype_id=1)
db.session.add(bp1)


db.session.commit()
