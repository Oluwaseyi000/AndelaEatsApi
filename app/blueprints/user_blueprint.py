from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Auth, Security
from app.controllers.user_controller import UserController
from flasgger import swag_from

user_blueprint = Blueprint('user', __name__, url_prefix='{}/users'.format(BaseBlueprint.base_url_prefix))
user_controller = UserController(request)


@user_blueprint.route('/admin', methods=['GET'])
@Auth.has_permission('create_user_roles')
@swag_from('documentation/get_all_admin_users.yml')
def list_admin_users():
    return user_controller.list_admin_users()


@user_blueprint.route('/', methods=['GET'])
@Auth.has_permission('view_users')
@swag_from('documentation/get_all_users.yml')
def list_all_users():
    return user_controller.list_all_users()


@user_blueprint.route('/<int:id>/', methods=['DELETE'])
@Auth.has_permission('delete_user')
@swag_from('documentation/delete_user.yml')
def delete_user(id):
    return user_controller.delete_user(id)


@user_blueprint.route('/', methods=['POST'])
@Auth.has_permission('create_user')
@Security.validator(
    ['slackId|optional', 'firstName|required', 'lastName|required',
     'userId|optional', 'imageUrl|optional:url'])
@swag_from('documentation/create_user.yml')
def create_user():
    return user_controller.create_user()
