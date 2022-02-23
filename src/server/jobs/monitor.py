import logging
from core.events import track_event

from scheduler import job
from core.metadata.task import RunAndAnalyzeTask
from core.models.monitor import MsiMonitor
from core.models.datasource import DataSource

from server.config import db_config as destination
from server.db import db

logger = logging.getLogger(__name__)


class MonitorJob(job.JobBase):
    MAX_RETRIES = 3
    TIMEOUT = 10

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': ('This runs the monitor assigned as an argument.'),
            'arguments': [
                # monitor_id
                {'type': 'integer', 'description': 'The ID of the monitor to run.'},
            ],
            'example_arguments': ('["#slack-bot-test", "ndscheduler chat bot", ":satisfied:",'
                                  ' "Standup, team! @channel"]')
        }

    def run(self, monitor_id, *args, **kwargs):
        track_event(action="monitor_start", label="server")

        # retrieve and save data - PipelineTask
        monitor = db.session.query(MsiMonitor).filter(MsiMonitor.id == monitor_id).one()
        source = db.session.query(DataSource).filter(DataSource.name == monitor.source).one()

        task = RunAndAnalyzeTask.from_source_and_destinations([monitor], source.db_config(), [destination])
        results = task.run()

        track_event(action="monitor_end", label="server")
