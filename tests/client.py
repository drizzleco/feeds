import os
import tempfile

import pytest

from app import create_app
from models import db


@pytest.fixture
def client():
    app = create_app()
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.secret_key = "sekrit!"
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client
    os.close(db_fd)
    os.unlink(app.config["DATABASE"])
