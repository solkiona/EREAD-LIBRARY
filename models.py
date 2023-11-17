
from db import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship 


#Association Table for Favorite Books 
favorite_books = db.Table(
    'favorite_books', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(100), nullable=False)
    bookAuthor = db.Column(db.String(100), nullable=False)
    # favorite = db.Column(db.Boolean, default=False)
    coverImage = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(1000), nullable=False)
    filepath = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    
    #Relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))
    user = relationship('User', back_populates='books')
    
    #Define a relationship with the favorite_books association table 
    favorites = relationship('User', secondary=favorite_books, back_populates='favorite_books')
    
    
    def __repr__(self):
        return f'<Book {self.bookTitle}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    books = relationship('Book', back_populates='user', cascade='all, delete-orphan')
    
    favorite_books = relationship('Book', secondary=favorite_books, back_populates='favorites')
    
    
    def __repr__(self):
        return f'<User {self.username}>'