from routes.user import users_bp
from routes.attendance import attendance_bp
from routes.verify_face import verify_face_bp

def register_routes(app):
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(verify_face_bp, url_prefix='/api/verify_face')
