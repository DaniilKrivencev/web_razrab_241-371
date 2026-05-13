from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def index():
    from .app import db, VisitLog, check_rights
    
    @check_rights('view_logs')
    def view_logs_logic():
        page = request.args.get('page', 1, type=int)
        query = VisitLog.query.order_by(VisitLog.created_at.desc())
        if current_user.role_obj.name == 'Пользователь':
            query = query.filter_by(user_id=current_user.id)
        pagination = query.paginate(page=page, per_page=10)
        return render_template('logs/index.html', logs=pagination.items, pagination=pagination)
    
    return view_logs_logic()

@reports_bp.route('/pages')
@login_required
def pages_stat():
    from .app import db, VisitLog, check_rights
    
    @check_rights('view_stats')
    def logic():
        stats = db.session.query(
            VisitLog.path, 
            func.count(VisitLog.id).label('count')
        ).group_by(VisitLog.path).order_by(func.count(VisitLog.id).desc()).all()
        return render_template('logs/pages.html', stats=stats)
    
    return logic()

@reports_bp.route('/users')
@login_required
def users_stat():
    from .app import db, VisitLog, User, check_rights
    
    @check_rights('view_stats')
    def logic():
        stats = db.session.query(
            User.id, User.last_name, User.first_name, User.middle_name,
            func.count(VisitLog.id).label('count')
        ).outerjoin(VisitLog, User.id == VisitLog.user_id).group_by(User.id).order_by(func.count(VisitLog.id).desc()).all()
        return render_template('logs/users.html', stats=stats)
    
    return logic()

@reports_bp.route('/export/<type>')
@login_required
def export_csv(type):
    from .app import db, VisitLog, User, check_rights
    
    @check_rights('view_stats')
    def logic():
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        if type == 'pages':
            writer.writerow(['No', 'Страница', 'Количество посещений'])
            stats = db.session.query(VisitLog.path, func.count(VisitLog.id)).group_by(VisitLog.path).all()
            for i, row in enumerate(stats, 1):
                writer.writerow([i, row[0], row[1]])
            filename = "pages_report.csv"
        else:
            writer.writerow(['No', 'Пользователь', 'Количество посещений'])
            stats = db.session.query(User.first_name, func.count(VisitLog.id)).outerjoin(VisitLog).group_by(User.id).all()
            for i, row in enumerate(stats, 1):
                name = row[0] if row[0] else "Гость"
                writer.writerow([i, name, row[1]])
            filename = "users_report.csv"
        output.seek(0)
        return Response(output.getvalue(), mimetype="text/csv", headers={"Content-disposition": f"attachment; filename={filename}"})

    return logic()
