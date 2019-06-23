import factory

from app.models.faq import Faq
from app.utils import db
from app.utils.enums import FaqCategoryType
from app.utils.id_generator import PushID


class FaqFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Faq
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n :PushID().next_id())
    category = FaqCategoryType.user_faq
    question = factory.Faker('sentence', nb_words=8)
    answer = factory.Faker('sentence', nb_words=20)
