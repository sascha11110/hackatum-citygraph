from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
import flaskext.couchdb




if __name__ == '__main__':
    
    app.config.update(
        DEBUG = True,
        COUCHDB_SERVER = 'http://localhost:5432/',
        COUCHDB_DATABASE = 'hackatum'
    )
    manager = flaskext.couchdb.CouchDBManager()
    migrate = Migrate(app, db)
    manager.add_viewdef(docs_by_author)
    manager.sync(app)

    manager.add_command('db', MigrateCommand)
    manager.run()
