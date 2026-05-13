from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from .models import db
from .repositories import CourseRepository, UserRepository, CategoryRepository, ImageRepository, ReviewRepository

user_repository = UserRepository(db)
course_repository = CourseRepository(db)
category_repository = CategoryRepository(db)
image_repository = ImageRepository(db)
review_repository = ReviewRepository(db)

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

def params():
    return { p: request.form.get(p) or None for p in COURSE_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }

@bp.route('/')
def index():
    pagination = course_repository.get_pagination_info(**search_params())
    courses = course_repository.get_all_courses(pagination=pagination)
    categories = category_repository.get_all_categories()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
@login_required
def new():
    course = course_repository.new_course()
    categories = category_repository.get_all_categories()
    users = user_repository.get_all_users()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')
    img = None
    course = None 

    try:
        if f and f.filename:
            img = image_repository.add_image(f)

        image_id = img.id if img else None
        course = course_repository.add_course(**params(), background_image_id=image_id)
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        categories = category_repository.get_all_categories()
        users = user_repository.get_all_users()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)
    
    last_reviews = review_repository.get_last_reviews(course_id)
    user_review = None
    if current_user.is_authenticated:
        user_review = review_repository.get_user_review(course_id, current_user.id)
    
    return render_template('courses/show.html', 
                           course=course, 
                           reviews=last_reviews,
                           user_review=user_review)

@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)
    
    sort_by = request.args.get('sort_by', 'new')
    page = request.args.get('page', 1, type=int)
    
    pagination = review_repository.get_reviews_pagination(course_id, sort_by=sort_by, page=page)
    
    user_review = None
    if current_user.is_authenticated:
        user_review = review_repository.get_user_review(course_id, current_user.id)

    return render_template('courses/reviews.html',
                           course=course,
                           pagination=pagination,
                           sort_by=sort_by,
                           user_review=user_review)

@bp.route('/<int:course_id>/reviews/add', methods=['POST'])
@login_required
def add_review(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)
    
    if review_repository.get_user_review(course_id, current_user.id):
        flash('Вы уже оставили отзыв к этому курсу.', 'warning')
        return redirect(url_for('courses.show', course_id=course_id))

    rating = request.form.get('rating', type=int)
    text = request.form.get('text')
    
    if rating is None or text is None:
        flash('Все поля формы должны быть заполнены.', 'danger')
        return redirect(url_for('courses.show', course_id=course_id))

    try:
        review_repository.add_review(course_id, current_user.id, rating, text)
        
        # Пересчет рейтинга курса
        course.rating_num += 1
        course.rating_sum += rating
        db.session.commit()
        
        flash('Ваш отзыв успешно добавлен!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при сохранении отзыва: {e}', 'danger')
        
    return redirect(url_for('courses.show', course_id=course_id))
@bp.route('/my-courses')
@login_required
def my_courses():
    courses = course_repository.get_user_courses(current_user.id)
    return render_template('courses/my_courses.html', courses=courses)

@bp.route('/<int:course_id>/delete', methods=['POST'])
@login_required
def delete(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)
    
    if course.author_id != current_user.id:
        flash('У вас недостаточно прав для удаления этого курса.', 'danger')
        return redirect(url_for('courses.index'))
    
    if course_repository.delete_course(course_id):
        flash(f'Курс "{course.name}" был успешно удален.', 'success')
    else:
        flash('Ошибка при удалении курса.', 'danger')
        
    return redirect(url_for('courses.my_courses'))
