#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from flask_restful import Resource, Api

from models import db, Article, User

app = Flask(__name__)
api = Api(app)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    response = make_response(
        articles, 
        200
        )

    return response

# @app.route('/articles/<int:id>', methods=['GET'])
# def show_article(id):
#     if 'page_views' not in session:
#         session['page_views'] = 0
#     session['page_views'] += 1

#     if session['page_views'] <= 3:
#         article = Article.query.filter_by(id=id).first()
#         if article is None:
#             return jsonify({'message': 'Article not found'}), 404

#         article_to_dict = article.to_dict()
#         response = make_response(jsonify(article_to_dict), 200)
#         return response
    
#     else:
#         response_body = {
#             "message" : "Maximum pageview limit reached"
#         }
        
#         return make_response(
#             response_body,
#             401
#         )

class Show_Article(Resource):
    def get(self, id):
        if 'page_views' not in session:
            session['page_views'] = 0
        session['page_views'] += 1

        if session['page_views'] <= 3:
            article = Article.query.filter_by(id = id).first()
            article_to_dict = article.to_dict()
            response = make_response(
                jsonify(article_to_dict),
                200
            )
            return response

        else: 
            response_body = {
                "message" : "Maximum pageview limit reached"
            }

            return make_response(
                response_body,
                401
            )
        

api.add_resource(Show_Article, '/articles/<int:id>')



if __name__ == '__main__':
    app.run(port=5555)
