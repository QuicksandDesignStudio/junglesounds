from .. import db

class Clasification(db.Model):
    __tablename__ = "classification"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    start_time = db.Column(db.Float, db.ForeignKey('category.id'))
    end_time = db.Column(db.Float, db.ForeignKey('category.id'))
