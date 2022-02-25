from sqlalchemy.orm import sessionmaker
from core.models.integrations.slack import SlackIntegration
from core.models.integration import Integration
from core.models.metadata.metric import MsiMetric

from core.models import mapper_registry

def upsert_data(entries_b, model, key, session):
    entries = {}
    for entry in entries_b:
        entries[str(entry['metric_id'])] = entry
    entries_to_update = []
    entries_to_insert = []
    
    # get all entries to be updated
    for each in session.query(model).filter(getattr(model, key).in_(entries.keys())).all():
        entry = entries.pop(str(getattr(each, key)))
        entries_to_update.append(entry)
        
    # get all entries to be inserted
    for entry in entries.values():
        entries_to_insert.append(entry)

    session.bulk_insert_mappings(model, entries_to_insert)
    # session.bulk_update_mappings(model, entries_to_update)

    session.commit()
    session.expunge_all()

class ZScoreLoader:
    def __init__(self, destinations):
        self.destinations = destinations

    def _alert(self, zscores, Session):
        # Send alerts for the above
        error_zscores = list(filter(lambda x: x.error, zscores))
        metric_ids = set([zscore.metric_id for zscore in error_zscores])

        if len(metric_ids) > 0:
            with Session() as session:
                integrations = session.query(Integration).all()
                for integration in integrations:
                    for id in metric_ids:
                        metric = session.query(MsiMetric).filter(MsiMetric.id == id).one()
                        for integration in integrations:
                            integration.send(metric)

    def _load(self, destination, zscores):
        from core.drivers.factory import load_driver

        driver_cls = load_driver(destination)
        driver = driver_cls(destination)

        driver._before_execute()
        mapper_registry.metadata.create_all(driver.engine)

        Session = sessionmaker(bind=driver.engine)
        with Session() as session:
            from core.models.zscore import ZScore
            upsert_data([zscore.to_dict() for zscore in zscores], ZScore, 'metric_id', session)

        self._alert(zscores, Session)

    def run(self, zscores):
        for destination in self.destinations:
            self._load(destination, zscores)
