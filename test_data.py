from app import db, app
from app.models import User, Post, Country, City, CityIntroduction, \
PicTest ,MemberItem




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

