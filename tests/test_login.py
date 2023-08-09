from tests.BaseCase import BaseCase

class TestUserLogin(BaseCase):
    def test_login_successful(self):
        self.client.post('/api/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )

        response = self.client.post('/api/auth/login',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )
        token_header = {
            'Authorization': f"Bearer {response.json.get('access_token')}",
        }
        self.assertEqual(response.status_code, 200)
        init_task = { 'task': 'task1', 'complete': False }
        task_create_resp = self.client.post('/api/task/create',
            json = init_task,
            headers = token_header
        )
        self.assertEqual(task_create_resp.status_code, 201)

        task_get_resp = self.client.get(
            '/api/task/',
            headers = token_header
        )
        self.assertEqual(task_get_resp.status_code, 200)
        self.assertEqual(task_get_resp.json[0], init_task)
        update_task = { 'task_id': 1, 'complete': True }
        task_update_resp = self.client.post(
            '/api/task/update',
            json = update_task,
            headers = token_header
        )
        self.assertEqual(task_update_resp.status_code, 200)
        task_get_resp = self.client.get(
            '/api/task/',
            headers = token_header
        )
        self.assertEqual(task_get_resp.json[0].get("complete"), update_task.get("complete"))
        second_task = { 'task': 'task2', 'complete': False }
        task_create_resp = self.client.post('/api/task/create',
            json = second_task,
            headers = token_header
        )
        self.assertEqual(task_create_resp.status_code, 201)
        task_get_resp = self.client.get(
            '/api/task/',
            headers = token_header
        )
        self.assertEqual(len(task_get_resp.json), 2)

        task_delete_resp = self.client.get(
            '/api/task/delete/1',
            headers = token_header
        )
        self.assertEqual(task_delete_resp.status_code, 200)
        task_get_resp = self.client.get(
            '/api/task/',
            headers = token_header
        )
        self.assertEqual(len(task_get_resp.json), 1)

        task_delete_resp = self.client.get(
            '/api/task/delete/2',
            headers = token_header
        )
        self.assertEqual(task_delete_resp.status_code, 200)
        task_get_resp = self.client.get(
            '/api/task/',
            headers = token_header
        )
        self.assertEqual(len(task_get_resp.json), 0)

    def test_login_with_invalid_email(self):
        self.client.post('/api/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )

        response = self.client.post('/api/auth/login',
            json = { 'email': 'adminuser@demo.com', 'password': 'testuser' }
        )
        self.assertEqual(response.status_code, 401)

    def test_login_with_invalid_password(self):
        self.client.post('/api/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )

        response = self.client.post('/api/auth/login',
            json = { 'email': 'testuser@demo.com', 'password': 'adminuser' }
        )
        self.assertEqual(response.status_code, 401)