import factory

from app.models.about import About
from app.utils import db
from app.utils.id_generator import PushID


class AboutFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = About
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n :PushID().next_id())
