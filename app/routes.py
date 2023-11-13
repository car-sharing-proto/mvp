def setup_routes(app):
    
    @app.route('/')
    def index():
        return 'This is the best carsharing backend!'