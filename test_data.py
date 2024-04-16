from app import db, app
from app.models import User, Post, Category, Location


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

japan = Location(name='japan')
shenzhen = Location(name='shenzhen')
macau = Location(name='macau')
taiwan = Location(name='taiwan')
thailand = Location(name='thailand')
korea = Location(name='korea')

tokyo = Location(name='tokyo', parent=japan)
osaka = Location(name='osaka', parent=japan)
kyoto = Location(name='kyoto', parent=japan)
kobe = Location(name='kobe ', parent=japan)
nara = Location(name='nara', parent=japan)
fukuoka = Location(name='fukuoka', parent=japan)
okinawa = Location(name='okinawa', parent=japan)
sapporo = Location(name='sapporo ', parent=japan)
nagoya = Location(name='nagoya ', parent=japan)
kumamoto = Location(name='kumamoto ', parent=japan)
hakone = Location(name='hakone ', parent=japan)
izu = Location(name='izu ', parent=japan)
tottori = Location(name='tottori ', parent=japan)
karuizawa = Location(name='karuizawa ', parent=japan)


db.session.add(japan)
db.session.add(taiwan)
db.session.add(macau)
db.session.add(tokyo)
db.session.add(osaka)
db.session.add(kyoto)
db.session.add(nara)
db.session.add(fukuoka)
db.session.add(okinawa)
db.session.add(sapporo)
db.session.add(nagoya)
db.session.add(kumamoto)
db.session.add(hakone)
db.session.add(izu)
db.session.add(tottori)
db.session.add(karuizawa)


db.session.commit()
