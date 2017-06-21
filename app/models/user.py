from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), index=True)
    state = db.Column(db.String(64))
    location = db.Column(db.String(64))
    topics = db.Column(db.PickleType)
    straight_query = db.Column(db.PickleType)
    category_query = db.Column(db.PickleType)


    def __init__(self, uid):
        self.uid = uid

    def set_state(self, state):
        self.state = state

    def set_location(self, location):
        self.state = location

    def set_topics(self, topics):
        self.topics = topics


    def set_straight_query(self, straight_query):
        self.straight_query = straight_query


    def set_category_query(self, category_query):
        self.category_query = category_query


    def __repr__(self):
        return '<User {} {} {} {}>'.format(self.uid, self.state, self.words, self.location)

