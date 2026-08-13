from flask import render_template
from flask_login import login_required, current_user

from app.schedule import bp
from app.models import Teacher, Subject, Room, Section, ScheduleEntry


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    stats = {
        'teachers': Teacher.query.filter_by(is_active=True).count(),
        'subjects': Subject.query.filter_by(is_active=True).count(),
        'rooms': Room.query.filter_by(is_active=True).count(),
        'sections': Section.query.filter_by(is_active=True).count(),
        'entries': ScheduleEntry.query.filter_by(status='active').count(),
    }
    return render_template('schedule/index.html', title='Dashboard',
                           stats=stats, user=current_user)
