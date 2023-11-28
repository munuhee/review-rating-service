"""
Module containing unit tests for Review routes.
"""
import unittest
from app import app, db
from app.models import Review

class TestReviewRoutes(unittest.TestCase):
    """Test case for reviewing routes."""

    def setUp(self):
        """Set up the testing environment"""
        app.config.from_pyfile('config.py')
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the testing environment"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_check(self):
        """Test health check endpoint."""
        with app.app_context():
            response = self.app.get('/health')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'healthy', response.data)

    def test_create_review(self):
        """Test creating a review"""
        with app.app_context():
            review_data = {
                'product_id': 1,
                'user_id': 1,
                'rating': 5,
                'comment': 'Great product!'
            }
            response = self.app.post('/reviews', json=review_data)
            self.assertEqual(response.status_code, 201)

            created_review = Review.query.filter_by(product_id=1, user_id=1).first()
            self.assertIsNotNone(created_review)
            self.assertEqual(created_review.rating, 5)
            self.assertEqual(created_review.comment, 'Great product!')

    def test_get_reviews_for_product(self):
        """Test retrieving reviews for a specific product"""
        with app.app_context():
            review_data = {
                'product_id': 2,
                'user_id': 3,
                'rating': 4,
                'comment': 'Nice product!'
            }
            self.app.post('/reviews', json=review_data)

            response = self.app.get('/products/2/reviews')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsNotNone(data['reviews'])
            self.assertEqual(len(data['reviews']), 1)

    def test_get_reviews_by_user(self):
        """Test retrieving reviews by a specific user"""
        with app.app_context():
            review_data = {
                'product_id': 4,
                'user_id': 5,
                'rating': 3,
                'comment': 'Okay product.'
            }
            self.app.post('/reviews', json=review_data)

            response = self.app.get('/users/5/reviews')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsNotNone(data['reviews'])
            self.assertEqual(len(data['reviews']), 1)

    def test_update_review(self):
        """Test updating a review"""
        with app.app_context():
            review_data = {
                'product_id': 6,
                'user_id': 7,
                'rating': 2,
                'comment': 'Not satisfied.'
            }
            self.app.post('/reviews', json=review_data)

            updated_data = {
                'rating': 1,
                'comment': 'Very disappointed.'
            }
            response = self.app.put('/reviews/1', json=updated_data)
            self.assertEqual(response.status_code, 200)

            updated_review = db.session.get(Review, 1)
            self.assertEqual(updated_review.rating, 1)
            self.assertEqual(updated_review.comment, 'Very disappointed.')

    def test_delete_review(self):
        """Test deleting a review"""
        with app.app_context():
            review_data = {
                'product_id': 8,
                'user_id': 9,
                'rating': 4,
                'comment': 'Satisfactory.'
            }
            self.app.post('/reviews', json=review_data)

            response = self.app.delete('/reviews/1')
            self.assertEqual(response.status_code, 200)

            deleted_review = db.session.get(Review, 1)
            self.assertIsNone(deleted_review)

    def test_get_single_review(self):
        """Test retrieving a single review by its ID"""
        with app.app_context():
            review_data = {
                'product_id': 10,
                'user_id': 11,
                'rating': 5,
                'comment': 'Excellent product!'
            }
            self.app.post('/reviews', json=review_data)

            response = self.app.get('/reviews/1')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['review_id'], 1)
            self.assertEqual(data['product_id'], 10)
            self.assertEqual(data['user_id'], 11)
            self.assertEqual(data['rating'], 5)
            self.assertEqual(data['comment'], 'Excellent product!')

if __name__ == '__main__':
    unittest.main()
