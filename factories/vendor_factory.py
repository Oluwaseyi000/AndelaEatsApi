from random import randint

import factory

from app.models.vendor import Vendor
from app.utils import db
from app.utils.id_generator import PushID

fake_tel = ''.join([str(randint(1, n)) for n in range(1, 12)])

class VendorFactory(factory.alchemy.SQLAlchemyModelFactory):


	class Meta:
		model = Vendor
		sqlalchemy_session = db.session

	id = factory.sequence(lambda n :PushID().next_id())
	name = factory.Faker('name')
	address = factory.Faker('address')
	tel = fake_tel
	contact_person = factory.Faker('name')
