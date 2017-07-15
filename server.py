## -*- coding: utf-8 -*-

from flask import Flask
from flask import request #para poder recibit parametros
from flask import request
from flask_wtf import CSRFProtect
from flask import session
from flask import jsonify
from flask import json
from flask import Response
from models import db
from models import Product
from models import ProductArticle
from models import ProductPicture
from models import ProductPictureArticle
from models import News
from models import User
from models import NewsArticle

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

from config import DevelopmentConfig

app = Flask(__name__) # creo la instancia
app.config.from_object(DevelopmentConfig)
CORS(app)



#app.secret_key = 'my_secret_key'
#csrf=CSRFProtect(app) #Para validar desde el frontend

def validateAuthorization(f):
    def auth(*args, **kwargs):

        #if request.endpoint is not 'signin' and request.endpoint is not 'signup':
        print request.method
        if request.method != 'GET' and request.endpoint != 'signup' and request.endpoint != 'signin':
            authorization = request.headers.get('Authorization')

            if authorization is None:
                return Response(json.dumps({
                    'message': 'Forbidden: Authorization key is missing'
                }), status=403, mimetype='application/json')
            else:
                user = User.query.filter_by(auth_token=authorization).first()
                if user is None:
                    return Response(json.dumps({
                        'message': 'Invalid token authorization'
                    }), status=404, mimetype='application/json')

        return f(*args, **kwargs)
    return auth

@app.before_request
@validateAuthorization
def before_request(): #Se ejecuta antes de que la peticion llegue al request
    pass

@app.after_request
def after_request(response): # Siempre recibe y devuelve un response
    return response

@app.route('/signup', methods=['POST'])
def signup():

    data = request.json

    user = User(
            data['fullname'],
            data['username'],
            data['email'],
            data['password']
        )

    db.session.add(user)
    db.session.commit()

    return Response(json.dumps({
        'message': 'User created'
    }), status=200, mimetype='application/json')


@app.route('/signin', methods=['POST'])
def signin():

    data = request.json

    user = User.query.filter_by(username=data['username']).first()

    if user is None:
        return Response(json.dumps({
            'message': 'User not found'
        }), status=404, mimetype='application/json')
    else:
        if check_password_hash(user.password, data['password']) == False:
            return Response(json.dumps({
                'message': 'Invalid credentials'
            }), status=404, mimetype='application/json')
        else:

            auth_token = generate_password_hash(user.password)

            user.auth_token = auth_token
            user.last_login = datetime.datetime.now()
            db.session.commit()

            return Response(json.dumps({
                'id': user.id,
                'fullname': user.fullname,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'auth_token': user.auth_token
            }), status=200, mimetype='application/json')

@app.route('/logout', methods=['POST'])
def logout():
    data = request.json

    user = db.session.query(User).filter_by(id=data['id'], username=data['username']).first()

    if user == None:
        return Response(json.dumps({
            'message': 'User not found'
        }), status=404, mimetype='application/json')

    user.auth_token = ''
    db.session.commit()

    return Response(json.dumps({
        'message': 'User logged out'
    }), 200, mimetype='application/json')

@app.route('/api/news/new', methods=['POST'])
def addNews():

    data =  request.json

    news = News()

    for article in data['articles']:
        newArticle = NewsArticle(
            title = article['title'],
            description = article['description'],
            lang = article['lang']
        )
        news.articles.append(newArticle)


    db.session.add(news)
    db.session.commit()

    return Response(json.dumps({
        'message': 'News has been created succesfully'
    }), status=200, mimetype='application/json')

# Esta ruta devuelve todas las noticias
@app.route('/api/news/', methods=['GET'])
#@cross_origin()
def getAllNews():

    all = db.session.query(News).order_by(News.id)
    data = []
    articles_list = []

    en = []
    es = []

    for news in all:
        articles = db.session.query(NewsArticle).filter_by(
            news_id=news.id
        )

        for article in articles:
            #articles_list.append({
            #    'id': article.id,
            #    'title': article.title,
            #    'description': article.description,
            #    'lang': article.lang,
            #})

            art = {
                'id': article.id,
                'title': article.title,
                'description': article.description
                #'lang': article.lang,
            }

            if(article.lang == 'en'):
                en.append(art)

            if(article.lang == 'es'):
                es.append(art)

        #data.append({
        #    'id': news.id,
        #    'articles': articles_list
        #})

        articles_list = []

    data.append({
        'en': en,
        'es': es,
    })

    return Response(json.dumps(data), status=200, mimetype='application/json')


@app.route('/api/news/<int:id>', methods=('GET', 'PUT', 'DELETE'))
def news(id):

    news = News.query.filter_by(id=id).first()

    # Si no hay ninguna noticia que tenga ese ID
    if news == None:
        return Response(json.dumps({
            'message': 'Not found'
        }), status=404, mimetype='application/json')

    # Si existe alguna noticia relacionada con el id
    if request.method == 'GET':

        articles_list = []
        articles = db.session.query(NewsArticle).filter_by(
            news_id=id
        )

        for article in articles:
            articles_list.append({
                'id': article.id,
                'title': article.title,
                'description': article.description,
                'lang': article.lang,
            })

        return Response(json.dumps({
            'id': news.id,
            'articles': articles_list
        }), status=200, mimetype='application/json')

    # Actualiza los campos que le llegan desde la request
    elif request.method == 'PUT':
        data = request.json

        for row in data['articles']:
            article = NewsArticle.query.filter_by(id=row['id']).first()

            article.title = row['title']
            article.description = row['description']
            article.lang = row['lang']

            db.session.commit()

        return Response(json.dumps({
            'message': 'News has been updated'
        }), status=200, mimetype='application/json')

    elif request.method == 'DELETE':

        db.session.delete(news)
        db.session.commit()

        return Response(json.dumps({
            'message': 'News has been removed'
        }), status=200, mimetype='application/json')

    else:
        pass


@app.route('/api/product/new', methods=['POST'])
def addProduct():

    data = request.json

    product = Product()

    for article in data['articles']:
        product_article = ProductArticle(
            title = article['title'],
            description = article['description'],
            lang = article['lang']
        )
        product.articles.append(product_article)

    for picture in data['pictures']:
        product_picture = ProductPicture(
            src=picture['src']
        )

        for article in picture['articles']:
            print article['title']
            product_picture_article = ProductPictureArticle(
                title = article['title'],
                description = article['description'],
                lang = article['lang']
            )
            product_picture.articles.append(product_picture_article)

        product.pictures.append(product_picture)

    db.session.add(product)
    db.session.commit()

    return Response(json.dumps({
        'message': 'Added a new product to database'
    }), status=200, mimetype='application/json')


# Esta ruta devuelve todos los productos
@app.route('/api/product/', methods=['GET'])
def getAllProducts():

    all = db.session.query(Product).order_by(Product.id)

    data = []

    pictures_data = []
    articles_data = []

    for product in all:

        articles = db.session.query(ProductArticle).filter_by(
            product_id=product.id
        )

        for article in articles:
            articles_data.append({
                'id': article.id,
                'title': article.title,
                'description': article.description,
                'lang': article.lang
            })


        pictures = db.session.query(ProductPicture).filter_by(
            product_id=product.id
        )

        for picture in pictures:

            picture_articles = []
            for article in picture.articles:
                picture_articles.append({
                    'id': article.id,
                    'product_picture_id': article.product_picture_id,
                    'title': article.title,
                    'description': article.description,
                })

            pictures_data.append({
                'id': picture.id,
                'src': picture.src,
                'articles': picture_articles
            })
            picture_articles = []

        data.append({
            'id': product.id,
            'pictures': pictures_data,
            'articles': articles_data
        })

        articles_data = []
        pictures_data = []

    return Response(json.dumps(data), status=200, mimetype='application/json')

@app.route('/api/product/<int:id>', methods=('GET', 'PUT', 'DELETE'))
def product(id):

    product = Product.query.filter_by(id=id).first()

    # Si no hay ninguna noticia que tenga ese ID
    if product == None:
        return Response(json.dumps({
            'message': 'Not found'
        }), status=404, mimetype='application/json')

    # Si existe alguna noticia relacionada con el id
    if request.method == 'GET':
        data = []

        pictures_data = []
        articles_data = []

        articles = db.session.query(ProductArticle).filter_by(
                product_id=product.id
        )

        for article in articles:
            articles_data.append({
                'id': article.id,
                'title': article.title,
                'description': article.description,
                'lang': article.lang
            })


        pictures = db.session.query(ProductPicture).filter_by(
                product_id=product.id
        )

        for picture in pictures:

            picture_articles = []
            for article in picture.articles:
                picture_articles.append({
                    'id': article.id,
                    'product_picture_id': article.product_picture_id,
                    'title': article.title,
                    'description': article.description,
                })

            pictures_data.append({
                'id': picture.id,
                'src': picture.src,
                'articles': picture_articles
            })
            picture_articles = []

        data.append({
            'id': product.id,
            'pictures': pictures_data,
            'articles': articles_data
        })

        articles_data = []
        pictures_data = []

        return Response(json.dumps(data[0]), status=200, mimetype='application/json')

    # Actualiza los campos que le llegan desde la request
    elif request.method == 'PUT':
        data = request.json

        for row_articles in data['articles']:
            article = ProductArticle.query.filter_by(id=row_articles['id']).first()
            article.title = row_articles['title']
            article.description = row_articles['description']
            article.lang = row_articles['lang']

            db.session.commit()

        for row_pictures in data['pictures']:
            productPicture = ProductPicture.query.filter_by(id=row_pictures['id']).first()
            productPicture.src = row_pictures['src']
            db.session.commit()

            for product_picture_article in row_pictures['articles']:
                productPictureArticle = ProductPictureArticle.query.filter_by(id=product_picture_article['id']).first()
                productPictureArticle.title = product_picture_article['title']
                productPictureArticle.description = product_picture_article['description']
                db.session.commit()


        return Response(json.dumps({
            'message': 'Product has been updated'
        }), status=200, mimetype='application/json')

    elif request.method == 'DELETE':

        db.session.delete(product)
        db.session.commit()

        return Response(json.dumps({
            'message': 'Product has been removed'
        }), status=200, mimetype='application/json')

    else:
        pass

@app.route('/static/who-we-are')
def whoWeAre():
    return json.dumps([{
        'en': {
            'description': 'We are an Argentine company that produces special connecting rods and transmissions for racing cars. Even though we specialize in high performance, we can also manufacture any type of connecting rod (whether it is for machines, ships, planes, trucks, among others) to satisfy the needs of our customers. Our products have won more than one hundred championships worldwide including 2 World Rally and one Fomula 1 Boat, with more than 50 years of experience and 40 in motor sports. Our goal is to fully satisfy the needs of our customers. We are proud to offer top quality products, custom-made with the latest technology. Everything is tested and retested at each stage of the manufacturing process to ensure our customers excellence.'
        },
        'es': {
            'description': ''
        }
    }])


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    #csrf.init_app(app)
    db.init_app(app)
    manager.run()
    with app.app_context(): # Bajo que contexto creo la app / sicncronizo bd y aplicacion
        db.create_all() # se encarga de crear toda slas tablas que no esten creadas
    app.run() # ejecuta el server, por default en el 5000


