"""Integration tests for the User Blueprint.
"""
from unittest.mock import patch

from tests.base_test_case import BaseTestCase
from app.utils.auth import PermissionRepo, UserRoleRepo
from factories import UserFactory, RoleFactory, PermissionFactory, UserRoleFactory
from .user_role import create_user_role


class TestUserEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    @patch.object(PermissionRepo,'get_unpaginated')
    @patch.object(UserRoleRepo, 'find_first')
    def test_get_admin_user_endpoint_with_right_permission(
        self,
        mock_user_role_repo_find_first,
        mock_permission_repo_get_unpaginated
        ):

        class MockUserRoleRep:
            def __init__(self, role_id):
                self.role_id = role_id

        class MockPermissionRepo:
            def __init__(self, keyword):
                self.keyword = keyword

        mock_user_role_repo = MockUserRoleRep(1)
        mock_user_perms = MockPermissionRepo("create_user_roles")

        with self.app.app_context():
            mock_user_role_repo_find_first.return_value = mock_user_role_repo
            mock_permission_repo_get_unpaginated.return_value = [mock_user_perms]

            response = self.client().get(self.make_url('/users/admin'), headers=self.headers())
            response = response.get_json()

            assert response['msg'] == 'OK'
            assert response['payload'].get('AdminUsers') == []

    def test_list_users_endpoint(self):
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_users', role_id=role.id)
        UserRoleFactory.create(user_id=user_id, role_id=role.id)

        # Create ten Dummy users
        UserFactory.create_batch(10)

        response = self.client().get(self.make_url('/users/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['users']), 10)
        self.assertJSONKeysPresent(payload['users'][0], 'firstName', 'lastName', 'slackId')

    def test_delete_user_endpoint_with_right_permission(self):
        user = UserFactory.create()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_user', role_id=role.id)
        UserRoleFactory.create(user_id=user_id, role_id=role.id)

        response = self.client().delete(self.make_url(f'/users/{user.id}/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['status'], 'success')
        self.assertEqual(response_json['msg'], 'User deleted')

    def test_delete_vendor_endpoint_without_right_permission(self):
        user = UserFactory.create()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='wrong_permission', role_id=100)
        UserRoleFactory.create(user_id=user_id, role_id=role.id)

        response = self.client().delete(self.make_url(f'/users/{user.id}/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')

    def test_delete_user_endpoint_with_wrong_user_id(self):
        user = UserFactory.create()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_user', role_id=role.id)
        UserRoleFactory.create(user_id=user_id, role_id=user.id)

        response = self.client().delete(self.make_url(f'/userrs/-576A/'), headers=self.headers())

        self.assert404(response)

    def test_create_user_endpoint_succeeds(self):

        create_user_role('create_user')
        user = UserFactory.build()

        user_data = dict(firstName=user.first_name, lastName=user.last_name)

        response = self.client().post(self.make_url("/users/"), headers=self.headers(),
                                      data=self.encode_to_json_string(user_data))

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['user']['firstName'], user.first_name)
        self.assertEqual(response_json['payload']['user']['lastName'], user.last_name)

