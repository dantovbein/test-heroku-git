from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import backref

import datetime

db = SQLAlchemy()

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    articles = db.relationship('NewsArticle', backref='news', lazy='dynamic', cascade="all,delete")

class NewsArticle(db.Model):
    __tablename__ = 'news_articles'

    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    title = db.Column(db.Text())
    description = db.Column(db.Text())
    lang = db.Column(db.String(2))

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    articles = db.relationship('ProductArticle', backref='products', lazy='dynamic', cascade="all,delete")
    pictures = db.relationship('ProductPicture', backref='products', lazy='dynamic', cascade="all,delete")
    product_category = db.Column(db.Integer, db.ForeignKey('product_picture_articles.id'))
    created_date = db.Column(db.DateTime, default= datetime.datetime.now)

class ProductArticle(db.Model):
    __tablename__ = 'product_articles'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    lang = db.Column(db.String(2))


class ProductPicture(db.Model):
    __tablename__ = 'product_pictures'

    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id')) # COn que tabla se relaciona
    src = db.Column(db.String(100))
    articles = db.relationship('ProductPictureArticle', backref='product_pictures', lazy='dynamic', cascade="all,delete")

class ProductPictureArticle(db.Model):
    __tablename__ = 'product_picture_articles'

    id = db.Column(db.Integer, primary_key = True)
    product_picture_id = db.Column(db.Integer, db.ForeignKey('product_pictures.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    lang = db.Column(db.String(2))

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(50))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(60))
    password = db.Column(db.String(100))
    auth_token = db.Column(db.String(100))
    role = db.Column(db.Integer, default=1)
    created_date = db.Column(db.DateTime, default= datetime.datetime.now)
    last_login = db.Column(db.DateTime)

    def __init__(self, fullname, username, email, password):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.password = self.__hasPassword(password)

    def __hasPassword(self, password):
        return generate_password_hash(password)

    def checkPasswordHash(self, password):
        return check_password_hash(self.password, password)

