import os
from snowplow_tracker import Tracker, AsyncEmitter, Subject, logger as snowplow_logger
import logging

snowplow_logger.setLevel(100)
SNOWPLOW_URL = "monosi-spipeline-collector-lb-1716143593.us-west-2.elb.amazonaws.com" 
send_anonymous_stats = os.getenv('SEND_ANONYMOUS_STATS', True)

e = AsyncEmitter(
    SNOWPLOW_URL, 
    protocol="http",
)
tracker = Tracker(
    e, 
    namespace="cf", 
    app_id="monosi",
)

def set_user_id(user_id):
    subject = Subject()
    subject.set_user_id(user_id)
    tracker.set_subject(subject)

def track_event(*args, **kwargs):
    if send_anonymous_stats == False:
        return

    try:
        tracker.track_struct_event(
            action=kwargs['action'],
            label=kwargs['label'],
            category='monosi',
        )
    except Exception as e:
        logging.error("Failed to send anonymous usage stats.")
        logging.error(e)

