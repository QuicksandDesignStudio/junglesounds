from app.main.start import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
	__tablename__ = "user"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(1024), unique=True, nullable=False)
	password = db.Column(db.String(1024), nullable=True)
	role = db.Column(db.String, nullable=True)
	approved = db.Column(db.Integer, nullable=True)

	def set_hash_password(self, password):
		self.password = generate_password_hash(password).decode('utf8')		

	def check_password(self, password):
		return check_password_hash(self.password, password)