from app import db, app
from app.models import Post, PostComment, Tag, User, BlogType, BlogPost, BlogComt, Country, City, CityIntroduction

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


#-----------------------------BlogPost----------------------------

p1 = BlogPost(id=1,title='JP',user_id=2 ,blogtype_id=1,description='JP is quite good')
p2 = BlogPost(id=2,title='TW',user_id=3 ,blogtype_id=1,description='TW is awsome')
p3 = BlogPost(id=3, title='Apple', user_id=4, blogtype_id=2, description='Apple is very good')
p4 = BlogPost(id=4, title='Orange', user_id=2, blogtype_id=2, description='Orange is very good')
p5 = BlogPost(id=5, title='Dog', user_id=3, blogtype_id=3, description='Dog is very good')
p6 = BlogPost(id=6, title='Cat', user_id=4, blogtype_id=3, description='Cat is very good')
db.session.add_all([p1,p2,p3,p4,p5,p6])

#-----------------------------BlogComt-----------------------------

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

#Add the Column to the Country Table
taiwan = Country(name='Taiwan')
japan = Country(name='Japan')

#Add the Colum to the City Table
taipei = City(id=1, name='Taipei', country=taiwan)
taichung = City(id=2, name='Taichung', country=taiwan)
tokyo = City(id=3, name='Tokyo', country=japan)
kyoto = City(id=4, name='Kyoto', country=japan)

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

db.session.commit()

# NewPost Mandy

t1 = Tag(id=1, name="Travel")
t2 = Tag(id=2, name="Gourmet")
db.session.add(t1)
db.session.add(t2)

b1 = Post(title="日本花季｜日本一年四季賞花時間表（附賞花景點推介） 4月櫻花、紫藤、粉蝶花｜6月繡球花｜7月8月薰衣草、向日葵 ", body='日本四季分明，一年365日春夏秋冬每個季節都有不少花卉植物可以欣賞，絕對不只有櫻花及紅葉！以下為大家整理日本一年四季的花季（12個月）、花期以及日本賞花景點推介，了解各種花卉開花時期。', city_id = 1, tag_id = 1, author=u1)
b2 = Post(title="福岡酒店推介｜博多The Lively HAKATA 三大看點！高質雙人房每晚人均$211起", body='Lively Hotels旗艦品牌「The Lively」一直主打富設計感、創新活力的精神酒店內外都裝修到極致豪華，位於城市區域的選址更加結合了該地的特色和人文精神。以下為你推介福岡的The Lively HAKATA，住宿雖然親民，但設施服務完全可媲美一般的商務酒店！最近計劃到九州遊覽的旅客，建議留意一下酒店詳情，儘快預訂！', city_id = 2, tag_id = 2, author=u2)
db.session.add(b1)
db.session.add(b2)

pc1 = PostComment(id=1, content='test',user_id=2 ,post_id=1)
pc2 = PostComment(id=2, content='test2',user_id=3 ,post_id=2)
db.session.add(pc1)
db.session.add(pc2)

db.session.commit()