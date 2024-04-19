from app import db, app
from app.models import Category, Blogger, BlogPost, User

app_context = app.app_context()
app_context.push()

db.engine.execute("DROP TABLE blogger CASCADE")
db.drop_all()
db.create_all()


u1 = User(username='1', email='1@gmail.com')
u1.set_password("1")
db.session.add(u1)


c1 = Category(name='HK')
c2 = Category(name='Travel')
db.session.add(c1)
db.session.add(c2)



bg1 = Blogger(id=1,name='John')
bg2 = Blogger(id=2,name='Alice')
bg3 = Blogger(id=3, name='Michael')
bg4 = Blogger(id=4, name='Emily')
bg5 = Blogger(id=5, name='Daniel')
db.session.add_all([bg1,bg2,bg3,bg4,bg5])


bp1 = BlogPost(id=1,blogger_id=1,title='JP',description='good')
#bp2 = BlogPost(id=2,blogger_id=2,title='HK',description='sheet')
db.session.add_all([bp1])


db.session.commit()
