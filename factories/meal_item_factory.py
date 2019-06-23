import factory
from app.utils import db
from random import randint
from app.utils.enums import MealTypes
from app.models.meal_item import MealItem
from app.utils.id_generator import PushID


class MealItemFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = MealItem
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: PushID().next_id())
    meal_type = MealTypes.side
    name = factory.Faker('name')
    image = 'https://www.pexels.com/photo/burrito-chicken-delicious-dinner-461198/'
