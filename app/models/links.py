from app import db


topic_to_ref_link = db.Table('topic_to_ref_link',
                             db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
                             db.Column('ref_id', db.Integer, db.ForeignKey('ref.id'))
                             )

topic_to_category_link = db.Table('topic_to_category_link',
                             db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
                             db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                             )
