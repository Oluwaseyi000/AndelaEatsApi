'''A module of location factory'''
import factory

from app.models import Location
from app.utils import db
from app.utils.id_generator import PushID


class LocationFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = Location
		sqlalchemy_session = db.session

	id = factory.sequence(lambda n :PushID().next_id())
	name = factory.Faker('name')
