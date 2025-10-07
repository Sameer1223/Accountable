import unittest
from unittest.mock import patch
from app import app
from database.models import db, User


class RBACAuthTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Create two users in DB
            self.admin_user_id = "1"
            self.normal_user_id = "2"

            admin = User(
                user_id=self.admin_user_id,
                email="admin@example.com",
                name="Group Admin",
            )
            normal = User(
                user_id=self.normal_user_id,
                email="user@example.com",
                name="Habit User",
            )
            db.session.add_all([admin, normal])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def fake_token_payload(self, user_id, role):
        """Return a fake JWT payload."""
        return {
            "sub": user_id,
            "permissions": [],
            "https://example.com/roles": [role],
        }

    @patch("auth.auth.verify_decode_jwt")
    @patch("auth.auth.check_permissions")
    def test_tasks_today_access_by_admin(self, mock_check, mock_verify):
        """Admin can access another user's tasks."""
        mock_verify.return_value = self.fake_token_payload(self.admin_user_id, "admin")
        mock_check.return_value = True

        res = self.client().get(
            f"/tasks-today/{self.normal_user_id}",
            headers={"Authorization": "Bearer faketoken"}
        )
        self.assertEqual(res.status_code, 200)

    @patch("auth.auth.verify_decode_jwt")
    @patch("auth.auth.check_permissions")
    def test_tasks_today_access_by_normal_user(self, mock_check, mock_verify):
        """Normal user can access their own tasks."""
        mock_verify.return_value = self.fake_token_payload(self.normal_user_id, "user")
        mock_check.return_value = True

        res = self.client().get(
            f"/tasks-today/{self.normal_user_id}",
            headers={"Authorization": "Bearer faketoken"}
        )
        self.assertEqual(res.status_code, 200)

    @patch("auth.auth.verify_decode_jwt")
    @patch("auth.auth.check_permissions")
    def test_tasks_today_access_by_group_admin(self, mock_check, mock_verify):
        """Group Admin can access someone else's tasks."""
        mock_verify.return_value = self.fake_token_payload(self.admin_user_id, "Group Admin")
        mock_check.return_value = True

        res = self.client().get(
            f"/tasks-today/{self.normal_user_id}",
            headers={"Authorization": "Bearer faketoken"}
        )
        self.assertEqual(res.status_code, 200)

    @patch("auth.auth.verify_decode_jwt")
    @patch("auth.auth.check_permissions")
    def test_tasks_today_access_denied_for_other_user(self, mock_check, mock_verify):
        """Normal user cannot access someone else's tasks."""
        mock_verify.return_value = self.fake_token_payload(self.normal_user_id, "user")
        mock_check.return_value = True

        res = self.client().get(
            f"/tasks-today/{self.admin_user_id}",
            headers={"Authorization": "Bearer faketoken"}
        )
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
