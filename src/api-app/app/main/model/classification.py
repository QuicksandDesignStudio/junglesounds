from app.main.start import db


class Classification(db.Model):
    __tablename__ = "classification"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'))
    sample = db.relationship("Sample")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship("Category")
    start_time = db.Column(db.Float)
    end_time = db.Column(db.Float)
