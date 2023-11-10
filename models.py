
from db import db
from sqlalchemy.sql import func



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(100), nullable=False)
    bookAuthor = db.Column(db.String(100), nullable=False)
    favorite = db.Column(db.Boolean, default=False)
    coverImage = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(1000), nullable=False)
    filepath = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f'<Book {self.bookTitle}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    
    def __repr_(self):
        return f'<User {self.username}>'