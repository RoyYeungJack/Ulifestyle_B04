from app import db, app
from app.models import User, Post , PicTest ,MemberItem


app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

u1 = User(username='john', email='john@example.com')
u2 = User(username='susan', email='susan@example.com')
test = User(username='test', email='test@test.com')
u1.set_password("P@ssw0rd")
u2.set_password("P@ssw0rd")
test.set_password("test")
db.session.add(u1)
db.session.add(u2)
db.session.add(test)
u1.follow(u2)
u2.follow(u1)

p1 = Post(body='my first post!', author=u1)
p2 = Post(body='my first post!', author=u2)
db.session.add(p1)
db.session.add(p2)


f1 = MemberItem(name='unbelievable curry fish ball', category='food', points=6969)
t1 = MemberItem(name='unbelievable japan travel', category='travel', points=6666)
db.session.add(f1)
db.session.add(t1)

cola = PicTest(name='cola', imglink='https://www.adweek.com/wp-content/uploads/files/2016_Jan/coke-taste-the-feeling-11.jpg.webp')
db.session.add(cola)


db.session.commit()
