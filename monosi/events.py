from snowplow_tracker import Tracker, AsyncEmitter, SelfDescribingJson, Subject, logger as snowplow_logger
import logging
import platform

snowplow_logger.setLevel(100)
SNOWPLOW_URL = "8345dd55-fcc1-402e-a7ef-cf044d2b8f02.app.try-snowplow.com" 
# check if dev
e = AsyncEmitter(
    SNOWPLOW_URL, 
    protocol="https",
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

def context():
    return [
        SelfDescribingJson(
            schema="iglu:com.trysnowplow/object/jsonschema/1-0-0",
            data={
                "name": "platform_context",
                "svalue": platform.platform(),
                # "svalue": platform.python_version(),
                # "svalue": platform.python_implementation(),
            },
        )
    ]

def track_event(config, *args, **kwargs):
    if config.send_anonymous_stats:
        try:
            tracker.track_struct_event(
                action=kwargs['action'],
                label=kwargs['label'],
                category='monosi',
                context=context(),
            )
        except Exception as e:
            logging.error("Failed to send anonymous usage stats.")
            logging.error(e)

