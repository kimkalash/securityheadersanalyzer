from app.models import User, Scan, HeaderResult
from app.db import SessionLocal 
import requests
from contextlib import contextmanager

def create_user(username: str, email: str, plain_password: str):
    session = SessionLocal()
    try:
        hashed_pw = hash_password(plain_password)  # 🔐 Secure hashing
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_pw
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_user_by_id(user_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    except Exception as e:
        session.rollback()
        raise 
    finally:
        session.close()

def create_scan(user_id: int, scan_url: str):
    session = SessionLocal()
    try:
        new_scan = Scan(
            user_id=user_id,
            scan_url=scan_url
        )
        session.add(new_scan)
        session.commit()
        session.refresh(new_scan)  # Refresh to get ID and scan_date
        return new_scan
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

from app.models import User  # if not already imported

def get_user_scans(user: User):
    session = SessionLocal()
    try:
        scans = session.query(Scan).filter(Scan.user_id == user.id).all()
        return scans
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_header_result(scan_id: int, header_name: str, header_value: str):
    session = SessionLocal()
    try:
        new_header_result = HeaderResult(
            scan_id=scan_id,
            header_name=header_name,
            header_value=header_value
        )
        session.add(new_header_result)
        session.commit()
        session.refresh(new_header_result)
        return new_header_result
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def analyze_headers(url: str) -> dict:
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        result = {h: headers.get(h, "Missing") for h in security_headers}
        return result
    except Exception as e:
        return {"error": str(e)}
@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
def run_scan_and_analyze(user_id: int, url: str):
    from datetime import datetime
    with get_db_session() as session:
        # 1. Create scan record
        new_scan = Scan(user_id=user_id, scan_url=url, scan_date=datetime.utcnow())
        session.add(new_scan)
        session.flush()  # get scan.id without commit

        # 2. Analyze headers
        try:
            response = requests.get(url, timeout=5)
            headers = response.headers
        except Exception as e:
            raise Exception(f"Failed to fetch headers: {str(e)}")

        # 3. Store results
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Permissions-Policy"
        ]
        for header in security_headers:
            value = headers.get(header, "Missing")
            session.add(HeaderResult(scan_id=new_scan.id, header_name=header, header_value=value))

        return {"scan_id": new_scan.id, "url": url, "headers": {h: headers.get(h, 'Missing') for h in security_headers}}
def delete_scan(scan_id: int):
    with get_db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise Exception("Scan not found")
        session.delete(scan)

def update_scan(scan_id: int, url: str):
    with get_db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise Exception("Scan not found")
        scan.scan_url = url