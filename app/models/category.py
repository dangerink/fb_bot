from app import db
from app.models.links import topic_to_category_link


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    topics = db.relationship('Topic', secondary=topic_to_category_link,
                                  backref=db.backref('categories', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)