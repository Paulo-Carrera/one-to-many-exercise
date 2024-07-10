# test_models.py

import unittest
from datetime import datetime
from app import app, db
from models import User, Post

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_user_model(self):
        with app.app_context():
            user = User(first_name="John", last_name="Doe", image_url=None)
            db.session.add(user)
            db.session.commit()
            
            self.assertEqual(user.first_name, "John")
            self.assertEqual(user.last_name, "Doe")
            self.assertEqual(user.image_url, "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
            self.assertEqual(len(User.query.all()), 1)

    def test_post_model(self):
        with app.app_context():
            user = User(first_name="John", last_name="Doe", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
            db.session.add(user)
            db.session.commit()

            post = Post(title="Test Post", content="Test content", user_id=user.id)
            db.session.add(post)
            db.session.commit()

            self.assertEqual(post.title, "Test Post")
            self.assertEqual(post.content, "Test content")
            self.assertEqual(post.user_id, user.id)
            self.assertIsInstance(post.created_at, datetime)
            self.assertEqual(len(Post.query.all()), 1)

if __name__ == '__main__':
    unittest.main()
