from app import db


class Topic(db.Model):
    __tablename__ = "topic"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Topic %r>' % (self.name)
