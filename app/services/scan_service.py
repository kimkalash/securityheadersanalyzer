# ----------- SCAN SERVICES -----------
def create_scan(db: Session, user_id: int, url: str, result: str):
    scan = models.Scan(user_id=user_id, url=url, result=result)
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

def get_scans_for_user(db: Session, user_id: int):
    return db.query(models.Scan).filter(models.Scan.user_id == user_id).all()

def delete_scan(db: Session, scan_id: int):
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if scan:
        db.delete(scan)
        db.commit()
    return scan
