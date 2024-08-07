from flask import Flask
from .extensions import db, ma, jwt, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/OnlineLearningDB'
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from .auth.routes import auth_bp
    from .courses.routes import courses_bp
    from .content.routes import content_bp
    from .forums.routes import forums_bp


    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(content_bp, url_prefix='/content')
    app.register_blueprint(forums_bp, url_prefix='/forums')

    return app
