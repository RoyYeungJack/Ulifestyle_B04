
from datetime import datetime, timedelta, timezone
from hashlib import md5
from app import app, db, login
import jwt
from sqlalchemy import Text
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, and_

from werkzeug.security import generate_password_hash, check_password_hash



followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean(), default=False)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    blog_postss = db.relationship('BlogPost', backref='user')
    blog_comtss = db.relationship('BlogComt', backref='user')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, followers.c.followed_id == Post.user_id
        ).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id,
                           "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)},
                          app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")[
                "reset_password"]
        except:           
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#---------------------Yeung Yau Ki(Jack) Table--------------------------------------
class BlogType(db.Model):
    __tablename__ = 'blogtype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10))
    blog_posts = db.relationship('BlogPost', backref='blogtype')


class BlogPost(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(600))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blogtype_id = db.Column(db.Integer, db.ForeignKey('blogtype.id'))
    blog_comts = db.relationship('BlogComt', backref='blogpost')

class BlogComt(db.Model):
    __tablename__ = 'blogcomt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blogpost_id = db.Column(db.Integer, db.ForeignKey('blogpost.id'))

#---------------------------------------------------------------------------------

#---------------------Mak Chun Kit(Gordy) Table-----------------------------------
  

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    cities = db.relationship('City', backref='country', lazy=True)

    def __repr__(self):
        return f'<Country {self.name}>'

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    posts = db.relationship('Post', backref='city', lazy='dynamic')

    def __repr__(self):
        return f'<City {self.name}>'
    
class CityIntroduction(db.Model):
    city_name = db.Column(db.String(50), db.ForeignKey('city.name'), primary_key=True)
    introduction = db.Column(Text)
    useful_links = db.Column(Text)
    emergency_help = db.Column(Text)
    transportation_info = db.Column(Text)
    climate = db.Column(Text)
    festivals = db.Column(Text)
    tags = db.Column(Text)
    related_content = db.Column(Text)
    image_path = db.Column(db.String(200))

    city = db.relationship('City', backref=db.backref('introduction', uselist=False))

    def __repr__(self):
        return f'<CityIntroduction {self.city_name}>'

class JapanPost(db.Model):
    __tablename__ = 'japan_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (CheckConstraint(and_(rating >= 1, rating <= 5), name='check_rating_range'),)

    author = db.relationship('User', backref='japan_posts')
#---------------------------------------------------------------------------------


#---------------------Chen Cho Cham(Tony) tables-----------------------------------
    
class UserPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, default=100)
    
    user = db.relationship('User')

    def add_points(user_id, points_to_add):
        user_points = UserPoints.query.filter_by(user_id=user_id).first()
        if user_points:
            user_points.points += points_to_add
            db.session.commit()
    def subtract_points(user_id, points_to_subtract):
        user_points = UserPoints.query.filter_by(user_id=user_id).first()
        if user_points and user_points.points >= points_to_subtract:
            user_points.points -= points_to_subtract
            db.session.commit()

class MemberItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    category = db.Column(db.String(64))  # 'food' or 'travel'
    points = db.Column(db.Integer)

class PicTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    imglink = db.Column(db.String(1000))

#--------------------------Lau Mei Yan (Mandy) tables-------------------------------

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    posts = db.relationship('Post', backref='tag', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Tag {self.body}>'

class Post(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    postcomment = db.relationship('PostComment', backref='post')

    def __repr__(self) -> str:
        return f'<Post {self.body}>'

class PostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self) -> str:
        return f'<PostComment {self.body}>'
    
#---------------------------------------------------------------------------