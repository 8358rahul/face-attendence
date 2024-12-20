from db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.Text, nullable=True)  # Store user photo path
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    attendances = db.relationship('Attendance', back_populates='user', cascade='all, delete-orphan')
