from app.main.start import db


class Sample(db.Model):
    __tablename__ = "sample"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sample_file_name = db.Column(db.String(1024), unique=True, nullable=False)
    file_hash = db.Column(db.String(512), unique=True, nullable=False)
    no_of_reviews = db.Column(db.Integer, nullable=False)
    classifications = db.relationship("Classification")