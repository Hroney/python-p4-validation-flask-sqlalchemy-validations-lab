from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def attributes_exist(self, key, address):
        if address:
            if not ((hasattr(self, key)) and (len(address) > 0)):
                raise ValueError(f"Must have {key} Attribute")
            elif Author.query.filter_by(name=address).first():
                raise ValueError("Must be unique name.")
            else:
                return address
        else:
            raise ValueError("Name cannot be empty.")
        

    @validates('phone_number')
    def phone_number_ten_digits(self, key, address):
        if address:
            if len(address) == 10 and address.isdigit():
               return address
            else:
                raise ValueError("Phone-Number must be 10 digits.")
        else:
            raise ValueError("Number cannot be empty")
            

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def title_validation(self, key, address):
        if address:
            clickbait_list = ["Won't Believe","Secret","Top","Guess"]
            if not any(clickbait in address for clickbait in clickbait_list):
                raise ValueError("Title not Click-baity")
            else:
                return address
        else:
            raise ValueError("Title cannot be empty")
        
    @validates('content')
    def content_length(self, key, address):
        if len(address) >= 250:
            return address
        else:
            raise ValueError("Content too long / empty")
        
    @validates('summary')
    def summary_length(self, key, address):
        if len(address) <= 250:
            return address
        else:
            raise ValueError("Summary too long")
        
    @validates("category")
    def category_check(self, key, address):
        if ((address == "Fiction") or (address == "Non-Fiction")):
            return address
        else:
            raise ValueError("Category must be Fiction or Non-Fiction")



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
