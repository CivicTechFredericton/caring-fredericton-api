from .error.routes import blueprint as error_bp
from .events.routes import blueprint as event_routes
from .guests.routes import blueprint as guest_routes
from .organizations.routes import blueprint as organization_routes
from .users.routes import blueprint as user_routes


def init_app(app):
    # Register the error handling endpoints
    app.register_blueprint(error_bp)

    # Register the REST API endpoints
    app.register_blueprint(event_routes)
    app.register_blueprint(guest_routes)
    app.register_blueprint(organization_routes)
    app.register_blueprint(user_routes)
