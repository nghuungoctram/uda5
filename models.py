import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

DATABASE_PATH = os.getenv('DATABASE_PATH')
db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/shirt-shop"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Shirt(db.Model):
    __tablename__ = 'shirt'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    color = Column(String(256), nullable=False)
    size = Column(String(256), nullable=False)
    link = Column(String(256), nullable=False)
    customer = db.relationship('Customer', backref='shirt', lazy=False)

    def __repr__(self):
        return f'<Shirt: {self.id}, name: {self.name}, color: {self.color}, size: {self.size}, link: {self.link}>'

    def __init__(self, name, color, size, link):
        self.name = name
        self.color = color
        self.size = size
        self.link = link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'size': self.size,
            'link': self.link
        }


class Customer(db.Model):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    gender = Column(String(500), nullable=False)
    phone = Column(Integer, nullable=False)
    shirt_id = db.Column(db.Integer, db.ForeignKey("shirt.id"), nullable=False)

    def __repr__(self):
        return f'<Customer: {self.id}, name: {self.name}, gender: {self.gender}, phone: {self.phone}, shirt_id: {self.shirt_id}>'

    def __init__(self, name, gender, phone, shirt_id):
        self.name = name
        self.gender = gender
        self.phone = phone
        self.shirt_id = shirt_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'phone': self.phone,
            'shirt_id': self.shirt_id
        }
