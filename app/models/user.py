from .base_model import BaseModel, db


class User(BaseModel):
    __tablename__ = 'users'

    slack_id = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String(100), nullable=True)
    user_type_id = db.Column(db.Integer(), db.ForeignKey('user_roles.id'))
    user_type = db.relationship('UserRole', lazy=False)
    image_url = db.Column(db.String, nullable=True)
