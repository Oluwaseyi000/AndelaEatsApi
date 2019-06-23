'''Factory module for generating fake instances of VendorRating class'''
import factory
import factory.fuzzy

from app.models import VendorRating
from app.utils import db
from app.utils.id_generator import PushID
from tests.base_test_case import BaseTestCase

from .vendor_engagement_factory import VendorEngagementFactory
from .vendor_factory import VendorFactory


class VendorRatingFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = VendorRating
        sqlalchemy_session = db.session

    vendor = factory.SubFactory(VendorFactory)
    engagement = factory.SubFactory(VendorEngagementFactory)

    id = factory.sequence(lambda n :PushID().next_id())
    vendor_id = factory.SelfAttribute('vendor.id')
    engagement_id = factory.SelfAttribute('engagement.id')
    user_id = BaseTestCase.user_id()
    service_date = factory.Faker('date_time')
    rating_type = 'order'
    comment = factory.Faker('sentence')
    rating = 4
    channel = factory.Faker('word')
