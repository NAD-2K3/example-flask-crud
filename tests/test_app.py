import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Entry


fake_entries = [
    {'id': 1, 'title': 'test title 1', 'description': 'test desc 1', 'status': True},
    {'id': 2, 'title': 'test title 2', 'description': 'test desc 2', 'status': False},
]

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # ✅ create all tables
        yield client
        with app.app_context():
            db.drop_all()  # cleanup

def test_home(client):
    # Insert sample data before hitting the route
    with app.app_context():
        entry = Entry(title='test title 1', description='test desc 1')
        db.session.add(entry)
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    assert b'test title 1' in response.data