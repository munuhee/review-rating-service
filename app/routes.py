"""Flask routes for managing product reviews.
Endpoints for creating, retrieving, updating, and deleting reviews, 
as well as retrieving reviews by product or user.
"""

from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from app import app, db
from app.models import Review

@app.route('/health', methods=['GET'])
def health_check():
    """health check returning a success status"""
    application_status = {
        'status': 'healthy'
    }
    return jsonify(application_status), 200

@app.route('/reviews', methods=['POST'])
def create_review():
    """
    Create a new review.

    Expects JSON data with 'product_id', 'user_id', and 'rating'.
    Returns a success message upon successful creation.
    """
    data = request.json
    if not all(key in data for key in ('product_id', 'user_id', 'rating')):
        return jsonify({'message': 'Missing required parameters'}), 400
    try:
        review = Review(
                product_id = data['product_id'],
                user_id = data['user_id'],
                rating = data['rating'],
                comment = data['comment']
                )
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create review', 'error': str(e)}), 500

@app.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_reviews_for_product(product_id):
    """
    Retrieve reviews for a specific product.

    Returns reviews associated with the provided product_id.
    """
    try:
        reviews = Review.query.filter_by(product_id=product_id).all()
        if not reviews:
            return jsonify({'message': 'No reviews found for this product'}), 404

        review_list = []
        for review in reviews:
            review_dict = {
                'review_id': review.review_id,
                'product_id': review.product_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'comment': review.comment
            }
            review_list.append(review_dict)

        return jsonify({'reviews': review_list}), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'Failed to retrieve reviews', 'error': str(e)}), 500


@app.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_reviews_by_user(user_id):
    """
    Retrieve reviews by a specific user.

    Returns reviews associated with the provided user_id.
    """
    try:
        reviews = Review.query.filter_by(user_id=user_id).all()
        if not reviews:
            return jsonify({'message': 'No reviews found for this user'}), 404

        review_list = []
        for review in reviews:
            review_dict = {
                'review_id': review.review_id,
                'product_id': review.product_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'comment': review.comment
            }
            review_list.append(review_dict)

        return jsonify({'reviews': review_list}), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'Failed to retrieve reviews', 'error': str(e)}), 500


@app.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update a specific review.

    Expects JSON data to update 'rating' and/or 'comment' of the review.
    """
    data = request.json
    try:
        review = db.session.get(Review, review_id)
        if not review:
            return jsonify({'message': 'Review not found'}), 404

        if 'rating' in data:
            review.rating = data['rating']
        if 'comment' in data:
            review.comment = data['comment']

        db.session.commit()
        return jsonify({'message': 'Review updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update review', 'error': str(e)}), 500

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a specific review.
    """
    try:
        review = db.session.get(Review, review_id)
        if not review:
            return jsonify({'message': 'Review not found'}), 404

        db.session.delete(review)
        db.session.commit()
        return jsonify({'message': 'Review deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete review', 'error': str(e)}), 500

@app.route('/reviews/<int:review_id>', methods=['GET'])
def get_single_review(review_id):
    """
    Retrieve a single review by its review_id.
    """
    try:
        review = db.session.get(Review, review_id)
        if not review:
            return jsonify({'message': 'Review not found'}), 404

        return jsonify({
            'review_id': review.review_id,
            'product_id': review.product_id,
            'user_id': review.user_id,
            'rating': review.rating,
            'comment': review.comment
        }), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'Failed to retrieve review', 'error': str(e)}), 500
