import os
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from core.security import log_tool_call

class OpenClawScheduler:
    def __init__(self, memory, registry):
        self.memory = memory
        self.registry = registry
        self.scheduler = BackgroundScheduler()
        self._setup_jobs()

    def _setup_jobs(self):
        """Initializes scheduled tasks."""
        # Daily Brief at 7:00 AM
        self.scheduler.add_job(
            self.daily_brief,
            CronTrigger(hour=7, minute=0),
            id='daily_brief'
        )

        # Email check every 15 minutes
        self.scheduler.add_job(
            self.check_emails,
            'interval',
            minutes=15,
            id='email_check'
        )

        # Deadline check every hour
        self.scheduler.add_job(
            self.check_deadlines,
            'interval',
            hours=1,
            id='deadline_check'
        )

        # Weekly Privacy Report - Sunday at 9 PM
        self.scheduler.add_job(
            self.privacy_report,
            CronTrigger(day_of_week='sun', hour=21, minute=0),
            id='privacy_report'
        )

    def start(self):
        self.scheduler.start()
        print("🕒 Scheduler started in background.")

    def stop(self):
        self.scheduler.shutdown()
        print("🕒 Scheduler stopped.")

    def _is_dnd_active(self) -> bool:
        """Checks if 'Do Not Disturb' is active based on memory."""
        dnd_hours = self.memory.get_fact("working_hours", "09:00-18:00")
        # Logic to skip if NOT in working hours or in sleep hours
        # For simplicity, we assume DND is active outside 7AM-10PM
        now = datetime.now().hour
        return now < 7 or now > 22

    def daily_brief(self):
        if self._is_dnd_active(): return
        print("\n🌅 Running Daily Brief...")
        # Placeholder for daily brief logic (weather, calendar, etc.)
        log_tool_call("scheduler", "DAILY_BRIEF", "Executed daily brief.")

    def check_emails(self):
        if self._is_dnd_active(): return
        # Placeholder for email checking logic
        pass

    def check_deadlines(self):
        # Always check deadlines
        # Placeholder for task deadline checks
        pass

    def privacy_report(self):
        print("\n📄 Generating Weekly Privacy Report...")
        log_tool_call("scheduler", "PRIVACY_REPORT", "Generated weekly privacy report.")
        # Logic to summarize access.log
