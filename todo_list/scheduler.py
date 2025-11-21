"""
Scheduled job utilities for the ToDo List application.

Provides commands to close overdue tasks once or on a recurring schedule.
"""

import time
from datetime import datetime
import schedule

from .storage import storage
from .config import config


def close_overdue_tasks_once() -> int:
    """Close overdue tasks and return the number of updated records."""
    updated = storage.close_overdue_tasks()
    print(f"[{datetime.utcnow().isoformat()}] Closed {updated} overdue tasks.")
    return updated


def run_scheduler() -> None:
    """Run the scheduler loop that closes overdue tasks periodically."""
    interval = config.close_overdue_interval_minutes
    print(f"Starting scheduler: closing overdue tasks every {interval} minute(s).")
    schedule.every(interval).minutes.do(close_overdue_tasks_once)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")


def main() -> None:
    """Entry point for running a single execution via CLI script."""
    close_overdue_tasks_once()


if __name__ == "__main__":
    main()
