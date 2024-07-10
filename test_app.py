# test_app.py

import unittest
from app import app, db
from models import User, Post

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            self.seed_data()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def seed_data(self):
        user1 = User(first_name="John", last_name="Doe", image_url=None)
        db.session.add(user1)
        db.session.commit()
        
        post1 = Post(title="First Post", content="This is the first post", user_id=user1.id)
        db.session.add(post1)
        db.session.commit()

    def test_home_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'users', response.data)

    def test_list_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_show_user(self):
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'First Post', response.data)

    def test_create_user(self):
        response = self.client.post('/users/new', data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'image_url': ''
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/users')
        self.assertIn(b'Jane Smith', response.data)

    def test_create_post(self):
        response = self.client.post('/users/1/posts/new', data={
            'title': 'Second Post',
            'content': 'This is the second post'
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/users/1')
        self.assertIn(b'Second Post', response.data)

if __name__ == '__main__':
    unittest.main()
