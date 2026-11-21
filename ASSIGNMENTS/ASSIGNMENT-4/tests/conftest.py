"""
Pytest fixtures for unit, integration, and regression testing.
Provides an isolated in-memory SQLite database, mock clocks, and pre-seeded roles.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.facility import Facility, FacilityPolicy
from app.models.user import User, UserRole
from app.security.authentication import create_access_token

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine, expire_on_commit=False
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


PRECOMPUTED_TEST_PASSWORD_HASH = "$2b$04$C6Bzns.91.pmHndhbUHf6OVBQv58TXGF626HERZcH3wk5m0C2S9ga"


@pytest.fixture(scope="function")
def seeded_users(db_session):
    """Seed users for all six roles to test authorization independently."""
    roles_data = [
        ("admin", "admin@campus.edu", UserRole.ADMINISTRATOR, "Central Administration"),
        ("manager_bob", "bob@campus.edu", UserRole.FACILITY_MANAGER, "Facilities Management"),
        ("tech_dave", "dave@campus.edu", UserRole.MAINTENANCE_TECHNICIAN, "Operations"),
        ("approver_alice", "alice@campus.edu", UserRole.DEPARTMENT_APPROVER, "Computer Science"),
        ("prof_smith", "smith@campus.edu", UserRole.FACULTY_MEMBER, "Computer Science"),
        ("student_charlie", "charlie@campus.edu", UserRole.STUDENT, "Computer Science"),
    ]
    users = {}
    for username, email, role, dept in roles_data:
        u = User(
            username=username,
            email=email,
            full_name=username.capitalize(),
            role=role,
            department=dept,
            hashed_password=PRECOMPUTED_TEST_PASSWORD_HASH,
            is_active=True,
        )
        db_session.add(u)
        users[username] = u
    db_session.commit()
    for u in users.values():
        db_session.refresh(u)
    return users


@pytest.fixture(scope="function")
def seeded_facilities(db_session):
    """Seed general and restricted facilities across campuses."""
    # Policies
    p_main = FacilityPolicy(
        campus="Main Campus", max_duration_minutes=180, temp_threshold=28.0, policy_version=1
    )
    p_north = FacilityPolicy(
        campus="North Campus", max_duration_minutes=120, temp_threshold=26.0, policy_version=1
    )
    db_session.add_all([p_main, p_north])
    db_session.flush()

    f1 = Facility(
        code="LAB-101",
        name="Computing Lab 101",
        campus="Main Campus",
        building="Turing Block",
        room_number="101",
        facility_type="Lab",
        capacity=40,
        is_restricted=False,
        policy_id=p_main.id,
    )
    f2 = Facility(
        code="RES-LAB-201",
        name="Advanced Robotics Research Lab",
        campus="Main Campus",
        building="Shannon Hall",
        room_number="201",
        facility_type="Research Lab",
        capacity=15,
        is_restricted=True,  # Restricted - requires approval
        policy_id=p_main.id,
    )
    db_session.add_all([f1, f2])
    db_session.commit()
    db_session.refresh(f1)
    db_session.refresh(f2)
    return {"general": f1, "restricted": f2, "policy_main": p_main, "policy_north": p_north}


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def make_auth_header(user: User) -> dict:
    """Helper to generate Authorization header for a user."""
    token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"Authorization": f"Bearer {token}"}
