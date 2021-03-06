from app.main.start import db


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(1024), unique=True, nullable=False)
    slug = db.Column(db.String(1024), unique=True, nullable=False)
