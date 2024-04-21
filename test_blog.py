from app import db, app
from app.models import User, BlogType, BlogPost, BlogComt

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


post1 = BlogPost(id=1,title='JP',description='good',user_id=1 ,blogtype_id=1)
post2 = BlogPost(id=2,title='apple',description='Bad',user_id=2 ,blogtype_id=2)
db.session.add_all([post1,post2])


comt1 = BlogComt(id=1, content='yo',user_id=1 ,blogpost_id=1)
comt2 = BlogComt(id=2, content='no yo',user_id=2 ,blogpost_id=2)
db.session.add_all([comt1,comt2])

db.session.commit()
