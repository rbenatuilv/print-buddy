import subprocess
from sqlmodel import Session, select
from ..db.main import engine
from .scheduler import scheduler


def check_cups() -> dict:
    """Check local CUPS connection and list available printers."""
    try:
        result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        if result.returncode == 0:
            printers = [
                line.split()[1] for line in result.stdout.splitlines() if line.startswith("printer")
            ]
            return {"status": "ok", "printers": printers}
        else:
            return {"status": "error", "message": result.stderr.strip() or "CUPS command failed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_database() -> dict:
    """Verify database connection and query execution."""
    try:
        with Session(engine) as session:
            session.exec(select(1)).first()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_scheduler() -> dict:
    """Check if the scheduler is running and list active jobs."""
    try:
        return scheduler.get_status()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def run_healthcheck() -> dict:
    """Run a complete system health check."""
    return {
        "cups": check_cups(),
        "database": check_database(),
        "scheduler": check_scheduler(),
    }

