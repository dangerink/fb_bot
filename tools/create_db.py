import re
import requests
from app import db
from app.models import Topic, Ref, Category
from app.models.user import User
from tools.logger import log
REIMPORT = 0 # set to True if need to reimport database
WIKI_URL = "https://en.wikipedia.org/wiki/Special:Export/"
INITIAL_THEMES = ["Data_science", "Machine_Learning", "computer", "Data_management"]

ref_types=dict(link='\[\[([a-z A-Z]*)\]\]',
               category='\[\[Category\:([a-z A-Z]*)\]\]')

def fetch(text, ref_type):

    parced = [item.replace(' ', '_' ).replace('|', '') for item in re.findall(ref_types[ref_type], text)]
    return set(parced)

def insert_topic(topic_name):
    log("creating record for topic {}".format(topic_name))
    topic = Topic(topic_name)
    db.session.add(topic)
    db.session.commit()
    return topic


def insert_ref(ref_name, topic):
    #log("creating record for ref {}".format(ref_name))
    ref = Ref.query.filter_by(name=ref_name).first()
    if not ref:
        ref = Ref(ref_name)
    ref.topics.append(topic)
    topic.refs.append(ref)
    db.session.commit()
    return ref

def insert_cat(cat_name, topic):
    #log("creating record for cat {}".format(cat_name))
    cat = Category.query.filter_by(name=cat_name).first()
    if not cat:
        cat = Category(cat_name)
    cat.topics.append(topic)
    topic.categories.append(cat)
    db.session.commit()
    return cat

def create_db(items):
    db.drop_all()
    db.create_all()

    topic_names = set()
    for theme in items:
        theme_data = requests.get(WIKI_URL + theme).text
        topic_names.update(fetch(theme_data, 'link'))

    log("fetching data on topics: {}".format(str(topic_names)))

    for topic_name in topic_names:
        topic = insert_topic(topic_name)
        topic_text = requests.get(WIKI_URL + topic_name).text

        refs_names = fetch(topic_text, 'link')
        log("got {} refs on {}.".format(len(refs_names), topic_name))
        for ref_name in refs_names:
            insert_ref(ref_name, topic)

        cat_names = fetch(topic_text, 'category')
        log("got {} cats on {}.".format(len(cat_names), ref_name))
        for cat_name in cat_names:
            insert_cat(cat_name, topic)
if __name__ == "__main__":

    try:
        User.__table__.drop(db.engine)
    except Exception:
        pass

    db.create_all()

    if REIMPORT:
        create_db(INITIAL_THEMES)

    result = {}
    for ref in Ref.query.filter(Ref.name.contains("relational")).all():
        if ref:
            result[ref.name] = [(top.name, [cat.name for cat in top.categories]) for top in ref.topics or []]

    print ({"text": str(result)})