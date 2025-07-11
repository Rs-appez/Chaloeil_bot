from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .question import Question


class QOTDScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.__init_schedule()
        self.__add_job()
        self.scheduler.start()

    def __init_schedule(self):
        job_default = {
            "coalesce": True,
            "max_instances": 3,
            "misfire_grace_time": 120,
        }
        self.scheduler.configure(
            job_defaults=job_default,
            timezone="Europe/Brussels",
        )

    def __add_job(self):
        self.scheduler.add_job(
            self.__create_qotd,
            CronTrigger(hour=18, minute=0),
            id="create_qotd",
        )

    def __create_qotd(self):
        Question.generate_questions_of_the_day()
