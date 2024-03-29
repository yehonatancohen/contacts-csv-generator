from flask import Flask, render_template
from flask_login import LoginManager
import sqlite3, os
#from util.decorators import guest_required 
from blueprints.home.home import home
#from blueprints.polls.polls import polls

def create_app():
    app = Flask(__name__, static_folder="blueprints/static")
    app.secret_key = 'your_secret_key_here'
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
    app.config['UPLOAD_EXTENTIONS'] = ['.xlsx', '.xls', '.csv', '.txt']
    app.config['UPLOAD_PATH'] = app.static_folder + '/uploads'    

    #login_manager = LoginManager(app)
    #login_manager.init_app(app)
    #login_manager.login_view = 'home.home' 

    with app.app_context():
        app.register_blueprint(home, url_prefix='/')
        #from blueprints.auth.auth import auth
        #app.register_blueprint(polls, url_prefix='/')
        #app.register_blueprint(auth, url_prefix='/')

    # connect to the database
    """try:
        db.init_tables()
    except sqlite3.OperationalError as e:
        print(e)
        pass"""
    
    """
    @app.errorhandler(500)
    def onError(error):
        return render_template('errorHandler.html', message="Sorry, something went wrong on our end<br>Refresh or come back later")

    @app.errorhandler(404)
    def onError(error):
        return render_template('errorHandler.html', message="Hey! This page doesn't appear to exist...<br>Go to the home page and try again")
    """
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')