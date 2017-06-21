from app.models.category import Category
from app.models.ref import Ref
from app.models.topic import Topic


class ModelHelper:

    def get_relevant_refs_topics(self, ref_names):
        result_topics = dict()
        for ref_name in ref_names:
            #refs = Ref.query.filter(Ref.name.contains(literal(ref_name)))
            refs = Ref.query.filter(Ref.name==ref_name).all()
            for ref in refs:
                for topic in ref.topics:
                    result_topics.setdefault(topic.name, []).append(ref.name)

        items = ((topic, len(references)) for topic, references in result_topics.items())
        sorted_topics = sorted(items, key=lambda item: item[1])
        return [item[0] for item in sorted_topics]

    def get_relevant_topics_cats(self, topic_names):
        result_cats = dict()
        for topic_name in topic_names:
            cats = Category.query.filter(Category.topics.any(name=topic_name)).all()
            for cat in cats:
                result_cats.setdefault(cat.name, []).append(topic_name)

        items = ((cat, len(topics)) for cat, topics in result_cats.items())
        sorted_cats = sorted(items, key=lambda item: item[1])
        return [item[0] for item in sorted_cats]

    def filter_topics_by_cat(self, topic_names, cat):
        topics = Topic.query.filter(Topic.name.in_(topic_names)).filter(Topic.categories.any(name=cat)).all()
        return [topic.name for topic in topics]

