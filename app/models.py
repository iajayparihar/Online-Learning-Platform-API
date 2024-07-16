from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable = False )
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(10), nullable = False )
    address = db.Column(db.String(255), nullable = False )


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # video, article, quiz
    content_url = db.Column(db.String(200), nullable=True)
    text_content = db.Column(db.Text, nullable=True)


class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

