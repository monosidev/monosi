import core.common.drivers.postgres
import core.common.drivers.redshift
import core.common.drivers.snowflake

from .base import BaseDriverConfiguration

class DriverFactory:
    def __init__(self):
        self._drivers = {}

        self._drivers['postgres'] = core.common.drivers.postgres
        self._drivers['redshift'] = core.common.drivers.redshift
        self._drivers['snowflake'] = core.common.drivers.snowflake
        # for entry_point in pkg_resources.iter_entry_points('monosi_drivers'):
        #     self._drivers[entry_point.name] = entry_point.load()

    def load_config_class(self, name: str):
        if name not in self._drivers.keys():
            raise Exception("Could not find driver specified: {}".format(name))

        return self._retrieve_driver_class(name, 'DriverConfiguration')

    def load_driver_class(self, config: BaseDriverConfiguration):
        name = config.driver_name()
        connection_cls = self._retrieve_driver_class(name, 'Driver')

        return connection_cls

    def _configuration(self, config_vals):
        driver_name = config_vals['driver']

        configuration_class = self._retrieve_driver_class(driver_name, 'DriverConfiguration')
        return configuration_class(**config_vals)

    def _retrieve_driver_class(self, driver_name, class_name):
        module = self._retrieve_driver_module(driver_name)
        return getattr(module, class_name)

    def _retrieve_driver_module(self, name):
        module = self._drivers.get(name)
        if not module:
            raise ValueError(name)
        return module


FACTORY: DriverFactory = DriverFactory()

def load_config(name: str):
    return FACTORY.load_config_class(name)

def load_driver(config: BaseDriverConfiguration):
    return FACTORY.load_driver_class(config)

