from tests.BaseCase import BaseCase

class TestUserSignup(BaseCase):
    def test_signup_successful(self):
        response = self.client.post('/api/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )
        token = response.json.get("token")
        self.assertEqual(response.status_code, 201)
        verify_resp = self.client.get(f'/api/auth/verify-email/{token}')
        self.assertEqual(verify_resp.status_code, 200)

    def test_signup_with_existing_email(self):
        self.client.post('/api/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )

        response = self.client.post('/api/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )
        self.assertEqual('User with given e-mail address already exists', response.json['message'])
        self.assertEqual(response.status_code, 400)

    def test_signup_invalid_email(self):
        response = self.client.post('/api/auth/signup',
            json = { 'email': 'testuser', 'password': 'testuser' }
        )
        self.assertEqual('E-mail address is invalid', response.json['message'])
        self.assertEqual(response.status_code, 400)

    # def test_signup_password_is_too_short(self):
    #     response = self.client.post('/api/v1/auth/signup',
    #         json = { 'email': 'testuser@demo.com', 'password': 'test' }
    #     )
    #     self.assertEqual('Password must be at least 6 characters', response.json['message'])
    #     self.assertEqual(response.status_code, 400)