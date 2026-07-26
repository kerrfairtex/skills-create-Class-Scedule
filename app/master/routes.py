from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

from app import db
from app.master import bp
from app.models import Teacher, TeacherAvailability, Subject, Room, Section, TeacherSubject

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('schedule.index'))
        return f(*args, **kwargs)
    return decorated


# ── Teachers ──────────────────────────────────────────────────────────────────

@bp.route('/teachers')
@login_required
def teachers():
    all_teachers = Teacher.query.filter_by(is_active=True).order_by(Teacher.last_name).all()
    return render_template('master/teachers.html', title='Teachers', teachers=all_teachers)


@bp.route('/teachers/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_teacher():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        specialization = request.form.get('specialization', '').strip()
        max_units = int(request.form.get('max_units', 21))

        if Teacher.query.filter_by(employee_id=employee_id).first():
            flash('Employee ID already exists.', 'danger')
        else:
            teacher = Teacher(
                employee_id=employee_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                specialization=specialization,
                max_units=max_units
            )
            db.session.add(teacher)
            db.session.commit()
            flash(f'Teacher {teacher.full_name} created.', 'success')
            return redirect(url_for('master.teachers'))

    return render_template('master/create_teacher.html', title='Add Teacher')


@bp.route('/teachers/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    subjects = Subject.query.filter_by(is_active=True).all()
    assigned_subject_ids = {ts.subject_id for ts in teacher.subject_assignments}

    if request.method == 'POST':
        teacher.first_name = request.form.get('first_name', '').strip()
        teacher.last_name = request.form.get('last_name', '').strip()
        teacher.email = request.form.get('email', '').strip()
        teacher.specialization = request.form.get('specialization', '').strip()
        teacher.max_units = int(request.form.get('max_units', 21))

        # Update subject assignments
        selected_subject_ids = set(
            int(sid) for sid in request.form.getlist('subjects')
        )
        # Remove unselected
        TeacherSubject.query.filter(
            TeacherSubject.teacher_id == teacher.id,
            TeacherSubject.subject_id.notin_(selected_subject_ids)
        ).delete(synchronize_session=False)
        # Add newly selected
        for sid in selected_subject_ids - assigned_subject_ids:
            db.session.add(TeacherSubject(teacher_id=teacher.id, subject_id=sid))

        # Update availability
        TeacherAvailability.query.filter_by(teacher_id=teacher.id).delete()
        avail_data = request.form.getlist('availability')
        for entry in avail_data:
            parts = entry.split(',')
            if len(parts) == 3:
                day, start, end = parts
                db.session.add(TeacherAvailability(
                    teacher_id=teacher.id,
                    day_of_week=int(day),
                    start_time=start.strip(),
                    end_time=end.strip()
                ))

        db.session.commit()
        flash('Teacher updated successfully.', 'success')
        return redirect(url_for('master.teachers'))

    return render_template('master/edit_teacher.html', title='Edit Teacher',
                           teacher=teacher, subjects=subjects,
                           assigned_subject_ids=assigned_subject_ids, days=DAYS)


@bp.route('/teachers/<int:teacher_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    teacher.is_active = False
    db.session.commit()
    flash(f'Teacher {teacher.full_name} deactivated.', 'success')
    return redirect(url_for('master.teachers'))


# ── Subjects ──────────────────────────────────────────────────────────────────

@bp.route('/subjects')
@login_required
def subjects():
    all_subjects = Subject.query.filter_by(is_active=True).order_by(
        Subject.year_level, Subject.semester, Subject.subject_code
    ).all()
    return render_template('master/subjects.html', title='Subjects', subjects=all_subjects)


@bp.route('/subjects/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_subject():
    if request.method == 'POST':
        subject_code = request.form.get('subject_code', '').strip().upper()
        subject_name = request.form.get('subject_name', '').strip()
        units = int(request.form.get('units', 3))
        hours_per_week = int(request.form.get('hours_per_week', 3))
        year_level = int(request.form.get('year_level', 1))
        semester = int(request.form.get('semester', 1))
        subject_type = request.form.get('subject_type', 'lecture')

        if Subject.query.filter_by(subject_code=subject_code).first():
            flash('Subject code already exists.', 'danger')
        else:
            subject = Subject(
                subject_code=subject_code,
                subject_name=subject_name,
                units=units,
                hours_per_week=hours_per_week,
                year_level=year_level,
                semester=semester,
                subject_type=subject_type
            )
            db.session.add(subject)
            db.session.commit()
            flash(f'Subject {subject_code} created.', 'success')
            return redirect(url_for('master.subjects'))

    return render_template('master/create_subject.html', title='Add Subject')


@bp.route('/subjects/<int:subject_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if request.method == 'POST':
        subject.subject_name = request.form.get('subject_name', '').strip()
        subject.units = int(request.form.get('units', 3))
        subject.hours_per_week = int(request.form.get('hours_per_week', 3))
        subject.year_level = int(request.form.get('year_level', 1))
        subject.semester = int(request.form.get('semester', 1))
        subject.subject_type = request.form.get('subject_type', 'lecture')
        db.session.commit()
        flash('Subject updated.', 'success')
        return redirect(url_for('master.subjects'))

    return render_template('master/edit_subject.html', title='Edit Subject', subject=subject)


@bp.route('/subjects/<int:subject_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    subject.is_active = False
    db.session.commit()
    flash(f'Subject {subject.subject_code} deactivated.', 'success')
    return redirect(url_for('master.subjects'))


# ── Rooms ─────────────────────────────────────────────────────────────────────

@bp.route('/rooms')
@login_required
def rooms():
    all_rooms = Room.query.filter_by(is_active=True).order_by(Room.room_code).all()
    return render_template('master/rooms.html', title='Rooms', rooms=all_rooms)


@bp.route('/rooms/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_room():
    if request.method == 'POST':
        room_code = request.form.get('room_code', '').strip().upper()
        room_name = request.form.get('room_name', '').strip()
        capacity = int(request.form.get('capacity', 40))
        room_type = request.form.get('room_type', 'classroom')
        building = request.form.get('building', '').strip()
        floor = int(request.form.get('floor', 1))

        if Room.query.filter_by(room_code=room_code).first():
            flash('Room code already exists.', 'danger')
        else:
            room = Room(
                room_code=room_code,
                room_name=room_name,
                capacity=capacity,
                room_type=room_type,
                building=building,
                floor=floor
            )
            db.session.add(room)
            db.session.commit()
            flash(f'Room {room_code} created.', 'success')
            return redirect(url_for('master.rooms'))

    return render_template('master/create_room.html', title='Add Room')


@bp.route('/rooms/<int:room_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)

    if request.method == 'POST':
        room.room_name = request.form.get('room_name', '').strip()
        room.capacity = int(request.form.get('capacity', 40))
        room.room_type = request.form.get('room_type', 'classroom')
        room.building = request.form.get('building', '').strip()
        room.floor = int(request.form.get('floor', 1))
        db.session.commit()
        flash('Room updated.', 'success')
        return redirect(url_for('master.rooms'))

    return render_template('master/edit_room.html', title='Edit Room', room=room)


@bp.route('/rooms/<int:room_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    room.is_active = False
    db.session.commit()
    flash(f'Room {room.room_code} deactivated.', 'success')
    return redirect(url_for('master.rooms'))


# ── Sections ──────────────────────────────────────────────────────────────────

@bp.route('/sections')
@login_required
def sections():
    all_sections = Section.query.filter_by(is_active=True).order_by(
        Section.year_level, Section.semester, Section.section_code
    ).all()
    return render_template('master/sections.html', title='Sections', sections=all_sections)


@bp.route('/sections/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_section():
    if request.method == 'POST':
        section_code = request.form.get('section_code', '').strip().upper()
        section_name = request.form.get('section_name', '').strip()
        year_level = int(request.form.get('year_level', 1))
        semester = int(request.form.get('semester', 1))
        student_count = int(request.form.get('student_count', 0))

        if Section.query.filter_by(section_code=section_code).first():
            flash('Section code already exists.', 'danger')
        else:
            section = Section(
                section_code=section_code,
                section_name=section_name,
                year_level=year_level,
                semester=semester,
                student_count=student_count
            )
            db.session.add(section)
            db.session.commit()
            flash(f'Section {section_code} created.', 'success')
            return redirect(url_for('master.sections'))

    return render_template('master/create_section.html', title='Add Section')


@bp.route('/sections/<int:section_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_section(section_id):
    section = Section.query.get_or_404(section_id)

    if request.method == 'POST':
        section.section_name = request.form.get('section_name', '').strip()
        section.year_level = int(request.form.get('year_level', 1))
        section.semester = int(request.form.get('semester', 1))
        section.student_count = int(request.form.get('student_count', 0))
        db.session.commit()
        flash('Section updated.', 'success')
        return redirect(url_for('master.sections'))

    return render_template('master/edit_section.html', title='Edit Section', section=section)


@bp.route('/sections/<int:section_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)
    section.is_active = False
    db.session.commit()
    flash(f'Section {section.section_code} deactivated.', 'success')
    return redirect(url_for('master.sections'))
