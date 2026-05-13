from ..models import Review
import sqlalchemy as sa

class ReviewRepository:
    def __init__(self, db):
        self.db = db

    def get_last_reviews(self, course_id, limit=5):
        query = sa.select(Review).filter_by(course_id=course_id).order_by(Review.created_at.desc()).limit(limit)
        return self.db.session.execute(query).scalars().all()

    def get_reviews_pagination(self, course_id, sort_by='new', page=1):
        query = sa.select(Review).filter_by(course_id=course_id)
        
        if sort_by == 'positive':
            query = query.order_by(Review.rating.desc(), Review.created_at.desc())
        elif sort_by == 'negative':
            query = query.order_by(Review.rating.asc(), Review.created_at.desc())
        else: # new
            query = query.order_by(Review.created_at.desc())
            
        return self.db.paginate(query, page=page, per_page=5)

    def get_user_review(self, course_id, user_id):
        return self.db.session.execute(
            sa.select(Review).filter_by(course_id=course_id, user_id=user_id)
        ).scalar_one_or_none()

    def add_review(self, course_id, user_id, rating, text):
        review = Review(
            course_id=course_id,
            user_id=user_id,
            rating=rating,
            text=text
        )
        self.db.session.add(review)
        return review
