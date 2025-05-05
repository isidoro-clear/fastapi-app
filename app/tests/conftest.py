from __future__ import annotations

import json
import pytest

from app.db import Base, TestingSessionLocal, engine_test, get_db
from app.main import app
from fastapi.testclient import TestClient

class ManifestDirectory(pytest.Directory):
    def collect(self):
        print(f"Collecting tests from {self.path}")
        manifest_path = self.path / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        ihook = self.ihook
        for file in manifest["files"]:
            file_path = self.path / file
            if file_path.is_file():
                yield from ihook.pytest_collect_file(file_path=file_path, parent=self)

@pytest.hookimpl
def pytest_collect_directory(path, parent):
    print(f"Collecting directory {path}")

    if path.joinpath("manifest.json").is_file():
        return ManifestDirectory.from_parent(parent=parent, path=path)
    return None

@pytest.fixture(scope="session", autouse=True)
def test_db_setup():
    # Drop all tables first to ensure clean state
    Base.metadata.drop_all(bind=engine_test)
    # Create all tables
    Base.metadata.create_all(bind=engine_test)
    yield
    # Clean up after all tests
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def db_session(test_db_setup):
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # app.dependency_overrides.clear()
