from app import db, app
from app.models import User, BlogType, BlogPost, BlogComt

app_context = app.app_context()
app_context.push()

#db.engine.execute("DROP TABLE BlogType CASCADE")

db.drop_all()
db.create_all()

#---------------------------User------------------------

u1 = User(id=1,username='admin', email='admin@gmail.com')
u2 = User(id=2,username='mary', email='2@gmail.com')
u3 = User(id=3,username='may', email='3@gmail.com')
u4 = User(id=4,username='john', email='1@gmail.com')
u1.is_admin = True

u1.set_password("admin")
u2.set_password("2")
u3.set_password("3")
u4.set_password("4")
db.session.add_all([u1,u2,u3,u4])


type1 = BlogType(id=1,type='Travel')
type2 = BlogType(id=2,type='Food')
type3 = BlogType(id=3,type='Pet')
db.session.add_all([type1,type2,type3])


#-----------------------------Post----------------------------

p1 = BlogPost(id=1,title='JP',user_id=1 ,blogtype_id=1,description='JP is quite good')
p2 = BlogPost(id=2,title='TW',user_id=2 ,blogtype_id=1,description='TW is awsome')
p3 = BlogPost(id=3, title='Apple', user_id=2, blogtype_id=2, description='Apple is very good')
p4 = BlogPost(id=4, title='Orange', user_id=2, blogtype_id=2, description='Orange is very good')
p5 = BlogPost(id=5, title='Dog', user_id=3, blogtype_id=3, description='Dog is very good')
p6 = BlogPost(id=6, title='Cat', user_id=3, blogtype_id=3, description='Cat is very good')
db.session.add_all([p1,p2,p3,p4,p5,p6])

#-----------------------------Comt-----------------------------

c1 = BlogComt(id=1, content='sound good',user_id=2 ,blogpost_id=1)
c2 = BlogComt(id=2, content='look good',user_id=3 ,blogpost_id=2)
c3 = BlogComt(id=3, content='not bad',user_id=4 ,blogpost_id=3)
c4 = BlogComt(id=4, content='thanks you',user_id=2, blogpost_id=4)
c5 = BlogComt(id=5, content='oh god',user_id=3, blogpost_id=5)
c6 = BlogComt(id=6, content='almost well',user_id=4, blogpost_id=6)
c7 = BlogComt(id=7, content='fine !',user_id=4 ,blogpost_id=1)
c8 = BlogComt(id=8, content='nonono',user_id=2 ,blogpost_id=2)
c9 = BlogComt(id=9, content='no problem',user_id=3 ,blogpost_id=3)
c10 = BlogComt(id=10, content='weak',user_id=4, blogpost_id=4)
c11 = BlogComt(id=11, content='shared',user_id=2, blogpost_id=5)
c12 = BlogComt(id=12, content='Oh',user_id=3, blogpost_id=6)
db.session.add_all([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12])

db.session.commit()
