from app import db, app
from app.models import User, Post, Category


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

p1 = Post(title="日本花季｜日本一年四季賞花時間表（附賞花景點推介） 4月櫻花、紫藤、粉蝶花｜6月繡球花｜7月8月薰衣草、向日葵 ", body='日本四季分明，一年365日春夏秋冬每個季節都有不少花卉植物可以欣賞，絕對不只有櫻花及紅葉！以下為大家整理日本一年四季的花季（12個月）、花期以及日本賞花景點推介，了解各種花卉開花時期。', author=u1)
p2 = Post(title="福岡酒店推介｜博多The Lively HAKATA 三大看點！高質雙人房每晚人均$211起", body='Lively Hotels旗艦品牌「The Lively」一直主打富設計感、創新活力的精神酒店內外都裝修到極致豪華，位於城市區域的選址更加結合了該地的特色和人文精神。以下為你推介福岡的The Lively HAKATA，住宿雖然親民，但設施服務完全可媲美一般的商務酒店！最近計劃到九州遊覽的旅客，建議留意一下酒店詳情，儘快預訂！', author=u2)
db.session.add(p1)
db.session.add(p2)

# Category add test
c1 = Category(name='HK')
c2 = Category(name='Travel')
db.session.add(c1)
db.session.add(c2)


db.session.commit()
