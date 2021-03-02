import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models


@pytest.fixture
def session():
    engine = create_engine("sqlite://", echo=False)
    session = sessionmaker(bind=engine)()
    models.User.__table__.create(engine, checkfirst=False)
    return session
