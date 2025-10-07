import unittest
from unittest.mock import patch
import json
from flask import abort, request
from jose import jwt
from app import app   # your global Flask app instance
from database.models import db, Group, Task, User

class APITestCase(unittest.TestCase):
    """This class represents the API test case"""

    def setUp(self):
        self.p_get_token = patch('auth.auth.get_token_auth_header', return_value='dummy-token')
        self.p_verify = patch('auth.auth.verify_decode_jwt', return_value={"permissions": [
            "get:groups","get:group-by-id","post:groups","get:tasks","get:tasks-today",
            "post:tasks","patch:tasks","delete:tasks","patch:add-user-to-group",
            "delete:user-group","get:users","patch:users"
        ]})
        self.p_check_perms = patch('auth.auth.check_permissions', return_value=True)

        # start patches
        self.mock_get_token = self.p_get_token.start()
        self.mock_verify = self.p_verify.start()
        self.mock_check_perms = self.p_check_perms.start()

        self.app = app
        self.client = self.app.test_client

        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True

        with self.app.app_context():
            db.create_all()
            u = User(user_id="u1", name="Tester", email="t@test.com")
            g = Group(g_id=1, g_name="G1", owner="u1")
            t = Task(id=1, name="Task1", user_id="u1", group_id=1, days="0123")
            db.session.add_all([u, g, t])
            db.session.commit()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.drop_all()

    # ---------- GROUP TESTS ----------
    def test_get_groups_success(self):
        res = self.client().get("/groups")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("groups", data)

    def test_get_group_by_id_success(self):
        res = self.client().get("/groups/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("group", data)

    def test_get_group_by_id_not_found(self):
        res = self.client().get("/groups/999")
        self.assertEqual(res.status_code, 404)

    def test_create_group_success(self):
        res = self.client().post("/groups", json={"name": "New Group", "owner": "u1"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_create_group_missing_field(self):
        res = self.client().post("/groups", json={"owner": "u1"})
        self.assertEqual(res.status_code, 400)

    # ---------- TASK TESTS ----------
    def test_get_tasks_success(self):
        res = self.client().get("/tasks")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("tasks", data)

    def test_get_task_by_id_success(self):
        res = self.client().get("/tasks/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("task", data)

    def test_get_task_by_id_not_found(self):
        res = self.client().get('/tasks/9999')  # non-existent ID
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_create_task_success(self):
        res = self.client().post("/tasks", json={"name": "X", "user_id": "u1"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_create_task_missing_field(self):
        res = self.client().post("/tasks", json={"name": "X"})
        self.assertEqual(res.status_code, 400)

    # ---------- USER TESTS ----------
    def test_get_users_success(self):
        res = self.client().get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("users", data)

    def test_get_user_by_id_success(self):
        res = self.client().get("/users/u1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("user", data)

    def test_get_user_by_id_not_found(self):
        res = self.client().get("/users/unknown")
        self.assertEqual(res.status_code, 422)

    def test_insert_user_success(self):
        res = self.client().post("/users", json={"user_id": "u2", "name": "X", "email": "x@test.com"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_insert_user_missing_name(self):
        res = self.client().post("/users", json={"user_id": "u3", "email": "x@test.com"})
        self.assertEqual(res.status_code, 400)

    def test_update_user_success(self):
        res = self.client().patch("/users/u1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_update_user_not_found(self):
        res = self.client().patch("/users/unknown")
        self.assertEqual(res.status_code, 422)




if __name__ == "__main__":
    unittest.main()
