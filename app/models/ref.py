from app import db
from app.models.links import topic_to_ref_link


class Ref(db.Model):
    __tablename__ = "ref"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    topics = db.relationship('Topic', secondary=topic_to_ref_link,
                                  backref=db.backref('refs', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Ref %r>' % (self.name)
