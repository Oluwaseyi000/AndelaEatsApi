from .base_model import BaseModel, db
from app.utils.enums import MealTypes


class MealItem(BaseModel):
    __tablename__ = 'meal_items'

    meal_type = db.Column(db.Enum(MealTypes))
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(1000))
    location_id = db.Column(db.String(80), db.ForeignKey('locations.id'), default=1)
    location = db.relationship('Location', lazy=False)
