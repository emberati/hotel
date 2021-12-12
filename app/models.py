from app import db
from sqlalchemy import Column, ForeignKey, Index, Integer, String, Date, Boolean, Float
from sqlalchemy import select
from flask_login import UserMixin

# TODO: Пересмотреть ассоциативные таблицы

sess = db.session

class Rent(db.Model):
    id              = Column(Integer, primary_key=True, nullable=False)
    room_id         = Column(Integer, ForeignKey('room.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    tenant_id       = Column(Integer, ForeignKey('tenant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    beg_of_period   = Column(Date, nullable=False)
    end_of_period   = Column(Date, nullable=False)

    # Relationships
    room = db.relationship('Room', back_populates='tenants')
    tenant = db.relationship('Tenant', back_populates='rooms')


class RoomService(db.Model):
    room_id     = Column(Integer, ForeignKey('room.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    staff_id    = Column(Integer, ForeignKey('staff.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)

    rooms = db.relationship('Room', back_populates='staff')
    staff = db.relationship('Staff', back_populates='rooms')


class Staff(db.Model):
    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    full_name       = Column(String(64), nullable=False)
    hiring_date     = Column(Date, nullable=False)
    dismissal_date  = Column(Date)

    rooms = db.relationship('RoomService', back_populates='staff')


class Room(db.Model):
    id          = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    busy        = Column(Boolean, index=True, nullable=False)
    cost        = Column(Float(precision=8), nullable=False)
    double_beds = Column(Integer, nullable=False)
    single_beds = Column(Integer, nullable=False)
    showers     = Column(Integer, nullable=False)
    toilets     = Column(Integer, nullable=False)

    # Relationships
    tenants = db.relationship('Rent', back_populates='room')
    staff = db.relationship('RoomService', back_populates='rooms')


class Tenant(db.Model):
    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id         = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),  nullable=False)
    full_name       = Column(String(64), nullable=False)
    doc_type        = Column(String(32), nullable=False)
    doc_number      = Column(String(32), unique=True, nullable=False)
    date_of_birth   = Column(Date, nullable=False)
    phone           = Column(String(11), unique=True)
    email           = Column(String(64), unique=True)

    rooms = db.relationship('Rent', back_populates='tenant')


class User(db.Model, UserMixin):
    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username        = Column(String(16), unique=True, nullable=False)
    pass_hash       = Column(String(32), nullable=False)

    # Relationships
    tenants         = db.relationship('Tenant', backref='user')

    # User session block

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    authenticated = False

    @property
    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return self.id

    @classmethod
    def from_db(cls, id: int = None, username: str = None):
        if id:
            stmt = select(User).where(User.id == id)
        elif username:
            stmt = select(User).where(User.username == username)
        else: raise AttributeError('Что-либо из id или username должно быть указано!')
        resp = sess.execute(stmt).scalars().first()

        if resp: return resp
        else: return False

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pass_hash, password)
