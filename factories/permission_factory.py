import factory
from app.utils import db
from app.models.permission import Permission
from factories.role_factory import RoleFactory
from app.utils.id_generator import PushID


class PermissionFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = Permission
		sqlalchemy_session = db.session
	
	id = factory.sequence(lambda n :PushID().next_id())
	name = factory.Faker('name')
	role_id = factory.SubFactory(RoleFactory)
	keyword = factory.Faker('word')
		
			