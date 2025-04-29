from app.models import User, Scan, HeaderResult
from app.db import SessionLocal

def create_user(username: str, email: str, password_hash: str):
    session = SessionLocal()
    try:
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # Refresh to get ID and timestamp
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

def get_user_scans(user_id: int):
    session = SessionLocal()
    try:
        scans = session.query(Scan).filter(Scan.user_id == user_id).all()
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
