from app import db, app
from app.models import Category, Blogger, Blogpost, User

app_context = app.app_context()
app_context.push()
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
db.session.add_all([bg1,bg2])


bp1 = Blogpost(id=1,blogger_id=1,name='P1')
bp2 = Blogpost(id=2,blogger_id=2,name='P2')
db.session.add_all([bp1,bp2])


db.session.commit()