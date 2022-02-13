import os

from cli.config import ProjectConfiguration
from cli.utils.yaml import write_file
 
from core.common.drivers.factory import load_driver
from core.common.drivers.factory import load_config
from .base import BaseCmd

from sqlalchemy.exc import OperationalError,DBAPIError
class PingCmd(BaseCmd):
  def run(self):
      source = self.args
      try:
          driver_config = self.config.sources[source]
          driver_cls = load_driver(driver_config)
          driver = driver_cls(driver_config)
          driver.test()
      except DBAPIError as err:
          print(f"Error Connecting to Data Source {err=}")
      except OperationalError as err:
          print(f"Invalid Source Configuration {err=}")
      except KeyError as err:
          print(f"Source \'{source}\' was not found. Must use one of: {list(self.config.sources.keys())}")
