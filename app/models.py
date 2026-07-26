from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# MOD-01: User model with RBAC (Admin, Faculty, Student)
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # admin, faculty, student
    full_name = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship('Teacher', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_faculty(self):
        return self.role == 'faculty'

    def is_student(self):
        return self.role == 'student'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# MOD-02: Teacher model (Faculty profiles with availability)
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(128))
    max_units = db.Column(db.Integer, default=21)  # maximum teaching load per semester
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='teacher')
    availability = db.relationship('TeacherAvailability', back_populates='teacher',
                                   cascade='all, delete-orphan')
    schedule_entries = db.relationship('ScheduleEntry', back_populates='teacher')
    subject_assignments = db.relationship('TeacherSubject', back_populates='teacher',
                                          cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<Teacher {self.full_name}>'


# MOD-02: Teacher availability slots
class TeacherAvailability(db.Model):
    __tablename__ = 'teacher_availability'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Mon, 1=Tue, ..., 4=Fri
    start_time = db.Column(db.String(5), nullable=False)  # HH:MM format
    end_time = db.Column(db.String(5), nullable=False)    # HH:MM format

    teacher = db.relationship('Teacher', back_populates='availability')

    __table_args__ = (
        db.UniqueConstraint('teacher_id', 'day_of_week', 'start_time', name='uq_teacher_availability'),
    )


# MOD-02: Subject / Curriculum model
class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(20), unique=True, nullable=False)
    subject_name = db.Column(db.String(128), nullable=False)
    units = db.Column(db.Integer, nullable=False, default=3)
    hours_per_week = db.Column(db.Integer, nullable=False, default=3)
    year_level = db.Column(db.Integer, nullable=False, default=1)  # 1-4
    semester = db.Column(db.Integer, nullable=False, default=1)     # 1-2
    subject_type = db.Column(db.String(20), default='lecture')      # lecture, lab
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher_assignments = db.relationship('TeacherSubject', back_populates='subject',
                                          cascade='all, delete-orphan')
    schedule_entries = db.relationship('ScheduleEntry', back_populates='subject')

    def __repr__(self):
        return f'<Subject {self.subject_code}: {self.subject_name}>'


# MOD-02: Teacher-Subject assignment (which teachers can teach which subjects)
class TeacherSubject(db.Model):
    __tablename__ = 'teacher_subjects'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)

    teacher = db.relationship('Teacher', back_populates='subject_assignments')
    subject = db.relationship('Subject', back_populates='teacher_assignments')

    __table_args__ = (
        db.UniqueConstraint('teacher_id', 'subject_id', name='uq_teacher_subject'),
    )


# MOD-02: Room / Facility model
class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(20), unique=True, nullable=False)
    room_name = db.Column(db.String(128), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=40)
    room_type = db.Column(db.String(20), default='classroom')  # classroom, laboratory
    building = db.Column(db.String(64))
    floor = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    schedule_entries = db.relationship('ScheduleEntry', back_populates='room')

    def __repr__(self):
        return f'<Room {self.room_code}>'


# MOD-02: Section model
class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    section_code = db.Column(db.String(20), unique=True, nullable=False)
    section_name = db.Column(db.String(128), nullable=False)
    year_level = db.Column(db.Integer, nullable=False, default=1)
    semester = db.Column(db.Integer, nullable=False, default=1)
    student_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    schedule_entries = db.relationship('ScheduleEntry', back_populates='section')

    def __repr__(self):
        return f'<Section {self.section_code}>'


# MOD-03/04/05: Schedule Entry - the core scheduling record
class ScheduleEntry(db.Model):
    __tablename__ = 'schedule_entries'

    id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.Integer, nullable=False, default=1)
    academic_year = db.Column(db.String(20), nullable=False, default='2024-2025')

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)

    day_of_week = db.Column(db.Integer, nullable=False)   # 0=Mon,...,4=Fri
    start_time = db.Column(db.String(5), nullable=False)   # HH:MM
    end_time = db.Column(db.String(5), nullable=False)     # HH:MM

    status = db.Column(db.String(20), default='active')    # active, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher = db.relationship('Teacher', back_populates='schedule_entries')
    subject = db.relationship('Subject', back_populates='schedule_entries')
    room = db.relationship('Room', back_populates='schedule_entries')
    section = db.relationship('Section', back_populates='schedule_entries')

    def __repr__(self):
        return f'<ScheduleEntry {self.subject.subject_code} {self.day_of_week} {self.start_time}-{self.end_time}>'


# MOD-04: Conflict log for tracking detected scheduling conflicts
class ConflictLog(db.Model):
    __tablename__ = 'conflict_logs'

    id = db.Column(db.Integer, primary_key=True)
    conflict_type = db.Column(db.String(50), nullable=False)  # room, teacher, section
    description = db.Column(db.Text, nullable=False)
    entry_1_id = db.Column(db.Integer, db.ForeignKey('schedule_entries.id'), nullable=True)
    entry_2_id = db.Column(db.Integer, db.ForeignKey('schedule_entries.id'), nullable=True)
    resolved = db.Column(db.Boolean, default=False)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<ConflictLog {self.conflict_type}: {self.description[:50]}>'
