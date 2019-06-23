import factory
from app.utils import db
from datetime import datetime
from app.models.meal_service import MealService
from app.utils.id_generator import PushID


class MealServiceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MealService
        sqlalchemy_session = db.session
        
    id = factory.sequence(lambda n :PushID().next_id())
    user_id = factory.Sequence(lambda n: n)
    session_id = factory.Sequence(lambda n: n)
    date = datetime.now()
