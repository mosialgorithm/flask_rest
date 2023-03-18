from db import db
from jdatetime import datetime



class ArticleModel(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    body = db.Column(db.Text())

    
    def __init__(self, title, body):
        self.title = title
        self.body = body
        
    def __repr__(self):
        return f'{self.id} - {self.title} - {self.body}'
    
    def json(self):
        return {'title':self.title, 'body':self.body}
    
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_form_db(self):
        db.session.delete(self)
        db.session.commit()
        
        