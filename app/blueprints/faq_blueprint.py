'''A module of FAQ blueprint'''
from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request
from app.controllers.faq_controller import FaqController
from app.utils.security import Security
from app.models import Faq
from flasgger import swag_from


faq_blueprint = Blueprint('faq', __name__, url_prefix='{}/faqs'.format(BaseBlueprint.base_url_prefix))

faq_controller = FaqController(request)


@faq_blueprint.route('/', methods=['GET'])
@Security.validate_query_params(Faq)
@swag_from('documentation/get_faqs.yml')
def list_faqs():

    kwargs = faq_controller.get_params_dict()

    return faq_controller.list_faqs(**kwargs)
