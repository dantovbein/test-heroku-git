

python sever.py db init
python sever.py db migrate
python sever.py db update

pip install MySQL-python
pip install Flask-Migrate



POST /signup
POST /signin
POST /logout

GET     /api/news
GET     /api/news/<id>
POST    /api/news/new
DELETE  /api/news/<id>
PUT     /api/news/<id>

GET     /api/product
GET     /api/product/<id>
POST    /api/product/new
PUT     /api/product/<id>
DELETE  /api/product/<id>


GET 
/api/news/<id>

```javascript

    {
        "articles": [
            {
                "description": <string:description>,
                "id": <integer:id>,
                "lang": <string:lang>,
                "title": <string:title>
            },
            {
                "description": "Esta es una descripciom",
                "id": 13,
                "lang": "es",
                "title": "Este es un titulo"
            }
        ],
        "id": 32
    }
```