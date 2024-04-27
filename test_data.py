from app import db, app
from app.models import User, Post, Country, City, CityIntroduction, \
PicTest, MemberItem


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


t1 = Tag(id=1, name="Travel")
t2 = Tag(id=2, name="Gourmet")
db.session.add(t1)
db.session.add(t2)

p1 = Post(title="日本花季｜日本一年四季賞花時間表（附賞花景點推介） 4月櫻花、紫藤、粉蝶花｜6月繡球花｜7月8月薰衣草、向日葵 ", body='日本四季分明，一年365日春夏秋冬每個季節都有不少花卉植物可以欣賞，絕對不只有櫻花及紅葉！以下為大家整理日本一年四季的花季（12個月）、花期以及日本賞花景點推介，了解各種花卉開花時期。', city_id = 1, tag_id = 1, author=u1)
p2 = Post(title="福岡酒店推介｜博多The Lively HAKATA 三大看點！高質雙人房每晚人均$211起", body='Lively Hotels旗艦品牌「The Lively」一直主打富設計感、創新活力的精神酒店內外都裝修到極致豪華，位於城市區域的選址更加結合了該地的特色和人文精神。以下為你推介福岡的The Lively HAKATA，住宿雖然親民，但設施服務完全可媲美一般的商務酒店！最近計劃到九州遊覽的旅客，建議留意一下酒店詳情，儘快預訂！', city_id = 2, tag_id = 2, author=u2)
db.session.add(p1)
db.session.add(p2)


#Add the Column to the Country Table
taiwan = Country(name='Taiwan')
japan = Country(name='Japan')

#Add the Colum to the City Table
taipei = City(name='Taipei', country=taiwan)
taichung = City(name='Taichung', country=taiwan)
tokyo = City(name='Tokyo', country=japan)
kyoto = City(name='Kyoto', country=japan)

# Session add all of the Country and City
db.session.add_all([taiwan, japan, tokyo, kyoto, taipei, taichung])

# create a new CityIntroduction instance
tokyo_intro = CityIntroduction(
    city_name='Tokyo',
    introduction= """
Tokyo

Tokyo, the capital of Japan, is located in the Kanto region of Honshu Island and is one of the three major financial centers of the world, alongside New York in the United States and London in the United Kingdom. Tokyo is primarily divided into 23 wards and 26 cities, covering an area of 2,162 square kilometers, approximately twice the size of Hong Kong, with a population of about 12.55 million. Although this represents only one-tenth of Japan's total population, Tokyo is a pivotal hub for Japan's development, featuring bustling commercial districts such as Shinjuku, Marunouchi, and Ginza.

Shinjuku is the most prosperous area in Tokyo, serving not only as a major commercial and tourist district but also as the city's transportation hub. The cultural contrast in Shinjuku is stark: on one side, there is the upscale commercial area which includes the Tokyo Metropolitan Government Building, whose observation decks are open to the public for free; on the other side is the famous red-light district—Kabukicho, known for its vibrant nightlife. The central area is a hub of department stores with famous names like Mitsukoshi, Isetan, and Marui.

Tokyo's prominent status in the fashion world draws many tourists eager to catch the latest trends, making it a shopping paradise. However, the city also preserves many historical landmarks, exemplifying the coexistence of old and new in a modern urban setting. Areas like Nihonbashi and Taito are excellent places to explore traditional Japanese architecture.
"""
)
kyoto_intro = CityIntroduction(
    city_name='Kyoto',
    introduction='Kyoto, originally established as Heian-kyo in 794 AD, served as the capital of Japan until the government relocated to Tokyo during the Meiji Restoration in 1868. It has a history spanning over 1,000 years, rich with precious Japanese traditional culture and historical architecture. Covering an area of about 820 square kilometers, Kyoto has a population of approximately 1.4 million.'
)

db.session.add_all([tokyo_intro,kyoto_intro])


#tables for member page items
f1 = MemberItem(name='unbelievable curry fish ball', category='food', points=6969)
t1 = MemberItem(name='unbelievable japan travel', category='travel', points=6666)
db.session.add(f1)
db.session.add(t1)

#link for ads pic
cola = PicTest(name='cola', imglink='https://www.adweek.com/wp-content/uploads/files/2016_Jan/coke-taste-the-feeling-11.jpg.webp')
db.session.add(cola)



db.session.commit()

