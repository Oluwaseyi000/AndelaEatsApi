from datetime import date, datetime, timedelta

import factory

from app.models.vendor_engagement import VendorEngagement
from app.utils import db
from app.utils.id_generator import PushID
from factories.vendor_factory import VendorFactory


#
# vendor = VendorFactory()
class VendorEngagementFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = VendorEngagement
		sqlalchemy_session = db.session

	vendor = factory.SubFactory(VendorFactory)
	
	id = factory.sequence(lambda n :PushID().next_id())
	vendor_id = factory.SelfAttribute('vendor.id')
	start_date = date.today()
	end_date = (datetime.now() + timedelta(weeks=+1)).date()
	status = 1
	termination_reason = factory.Faker('paragraph')
	# cohort_position = fake_cohort_position
