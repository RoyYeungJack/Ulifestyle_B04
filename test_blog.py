from app import db, app
from app.models import User, BlogType, BlogPost, BlogComt

app_context = app.app_context()
app_context.push()

#db.engine.execute("DROP TABLE BlogType CASCADE")

db.drop_all()
db.create_all()


u1 = User(id=1,username='John', email='1@gmail.com')
u2 = User(id=2,username='Mary', email='2@gmail.com')
u3 = User(id=3,username='May', email='3@gmail.com')
u1.set_password("1")
u2.set_password("2")
db.session.add_all([u1,u2,u3])


type1 = BlogType(id=1,type='Travel')
type2 = BlogType(id=2,type='Food')
type3 = BlogType(id=3,type='Pet')
type4 = BlogType(id=3,type='Girl')
db.session.add_all([type1,type2,type3])


p1 = BlogPost(id=1,title='JP',user_id=1 ,blogtype_id=1,description='JP is quite good')
p2 = BlogPost(id=2,title='TW',user_id=2 ,blogtype_id=1,description='TW is awsome')
p3 = BlogPost(id=3, title='Apple', user_id=2, blogtype_id=2, description='Apple is very good')
p4 = BlogPost(id=4, title='Orange', user_id=2, blogtype_id=2, description='Orange is very good')
p5 = BlogPost(id=5, title='Dog', user_id=3, blogtype_id=3, description='Dog is very good')
p6 = BlogPost(id=6, title='Cat', user_id=3, blogtype_id=3, description='Cat is very good')
db.session.add_all([p1,p2,p3,p4,p5,p6])


comt1 = BlogComt(id=1, content='sound good',user_id=1 ,blogpost_id=1)
comt2 = BlogComt(id=2, content='oh no',user_id=2 ,blogpost_id=2)
db.session.add_all([comt1,comt2])

db.session.commit()
