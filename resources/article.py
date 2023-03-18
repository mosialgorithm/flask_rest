from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.article import ArticleModel



class Article(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('body', type=str, required=True, help='this field must be fill')
    

    def get(self, title):
        article = ArticleModel.find_by_title(title)
        if article:
            return article.json()
        return {'message':'article not Found'}, 404
    
    
    def post(self, title):
        if ArticleModel.find_by_title(title):
            return {'message':'this article by title already exists'}, 400
        data = Article.parser.parse_args()
        article = ArticleModel(title, data['body'])
        print(article)
        try:
            article.save_to_db()
        except:
            return {'message':'An Error occured insertin the article'}, 500
        
        return article.json(), 201
    
    def put(self, title):
        article = ArticleModel.find_by_title(title)
        if article:
            data = Article.parser.parse_args()
            article.body = data['body']
            try:
                article.save_to_db()
                return {'message':f'Article by title _{title}_ is updatetd'}
            except:
                return {'message':'An Error is occured during inser the article'}
        else:
            return {'messasge':'this title is not in our article yet'}
    
    
    def delete(self, title):
        article = ArticleModel.find_by_title(title)
        if article:
            article.delete_form_db()
            return {'message':f'article with title _{title}_ is deleted successfully'}, 200
        else:
            return {'message' : f'article with title _{title}_ is not in database'}, 404
    
    
    
class Articles(Resource):
    
    @jwt_required()
    def get(self):
        # return {'articles' : list(article.json() for article in ArticleModel.query.all())}
        return {'Articles':list(map(lambda x:x.json(), ArticleModel.query.all()))}
    