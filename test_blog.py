from app import db, app
from app.models import Category, Blogger, BlogPost, User , BlogType

app_context = app.app_context()
app_context.push()

#db.engine.execute("DROP TABLE blogger CASCADE")
#db.engine.execute("DROP TABLE blogtype CASCADE")

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
bg3 = Blogger(id=3,name='Michael')
db.session.add_all([bg1,bg2,bg3])


bt1 = BlogType(id=1,type='Travel')
bt2 = BlogType(id=2,type='FOOD')
db.session.add_all([bt1,bt2])


bp1 = BlogPost(id=1,title='JP',description='good',blogger_id=3,blogtype_id=1)
db.session.add(bp1)


db.session.commit()
