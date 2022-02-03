from snowplow_tracker import Tracker, AsyncEmitter, SelfDescribingJson, Subject, logger as snowplow_logger
import logging
import platform

snowplow_logger.setLevel(100)
SNOWPLOW_URL = "monosi-spipeline-collector-lb-1716143593.us-west-2.elb.amazonaws.com" 
# check if dev
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

def context():
    # data = {
    #     "name": "platform_context",                
    #     "vendor": platform.platform(),
    #     "version": platform.python_version(),
    #     "format": platform.python_implementation(),
    # }
    return [
        SelfDescribingJson(
            schema="iglu:com.snowplowanalytics.self-desc/instance/jsonschema/1-0-0",
            data={},
            vendor=platform.platform(),
            name="platform_context",
            format=platform.python_implementation(),
            version=platform.python_version(),
        )
    ]

def track_event(config, *args, **kwargs):
    # if not config.send_anonymous_stats:
    #   return
    try:
        tracker.track_struct_event(
            action=kwargs['action'],
            label=kwargs['label'],
            category='monosi',
            # context=context(),
        )
    except Exception as e:
        logging.error("Failed to send anonymous usage stats.")
        logging.error(e)

