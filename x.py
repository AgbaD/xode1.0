#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from app import create_app, db
from app.models import Admin, Userlogs, Handbook
from flask_migrate import Migrate
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, app=app, Admin=Admin, Userlogs=Userlogs, Handbook=Handbook)


if __name__ == "__main__":
    app.run(debug=True)
