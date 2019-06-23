import factory

from app.models.role import Role
from app.utils import db
from app.utils.id_generator import PushID


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = Role
		sqlalchemy_session = db.session
	
	id = factory.sequence(lambda n :PushID().next_id())
	name = factory.Faker('word')
	help = 'A Help Message'
