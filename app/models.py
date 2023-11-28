"""Module containing Review class for handling review data."""

from app import db

class Review(db.Model):
    """Represents individual reviews."""

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    def __repr__(self):
        """String representation of a Review object."""
        return f"<Review {self.review_id}>"
