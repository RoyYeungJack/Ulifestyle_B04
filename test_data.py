from app import db, app
from app.models import User, Post, Category, Country, City


app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

u1 = User(username='john', email='john@example.com')
u2 = User(username='susan', email='susan@example.com')
u1.set_password("P@ssw0rd")
u2.set_password("P@ssw0rd")
db.session.add(u1)
db.session.add(u2)
u1.follow(u2)
u2.follow(u1)

p1 = Post(body='my first post!', author=u1)
p2 = Post(body='my first post!', author=u2)
db.session.add(p1)
db.session.add(p2)

# Category add test
c1 = Category(name='HK')
c2 = Category(name='Travel')
db.session.add(c1)
db.session.add(c2)
#db.create_all()


taiwan = Country(name='Taiwan')
japan = Country(name='Japan')

taipei = City(name='Taipei', country=taiwan)
taichung = City(name='Taichung', country=taiwan)
tokyo = City(name='Tokyo', country=japan)
kyoto = City(name='Kyoto', country=japan)

db.session.add_all([taiwan, japan, tokyo, kyoto, taipei, taichung])
db.session.commit()