import factory
from app.utils import db
from datetime import datetime, time, timedelta
from app.models.meal_session import MealSession
from app.utils.id_generator import PushID

class MealSessionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MealSession
        sqlalchemy_session = db.session
        force_flush = True
    
    id = factory.sequence(lambda n :PushID().next_id())
    name = 'breakfast'
    start_time = time(hour=8)
    stop_time =  time(hour=10, minute=30)
    date = datetime.now()
    location_id = factory.Sequence(lambda n: n)
    is_deleted = False
