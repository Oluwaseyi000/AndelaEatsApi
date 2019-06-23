import factory

from app.models.user import User
from app.utils import db
from app.utils.id_generator import PushID


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n :PushID().next_id())
    slack_id = factory.Sequence(lambda n: n)
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    user_id = factory.Faker('word')
    user_type_id = factory.Sequence(lambda n: n)
    image_url = factory.Faker('url')
