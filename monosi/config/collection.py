from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
import glob
import os

from monosi.drivers import DriverConfig
import monosi.utils.yaml as yaml

DEFAULT_COLLECTIONS_DIR = os.path.join(os.path.expanduser('~'), '.monosi')

@dataclass(init=False)
class CollectionConfigurationBase:
    config: DriverConfig
    collection_env_vars: Dict[str, Any]

@dataclass(init=False)
class CollectionConfiguration:
    def __init__(
        self,
        config: DriverConfig,
    ):
        self.config = config
        self.collection_env_vars = {}

    @classmethod
    def from_driver_config(
        cls,
        config: DriverConfig,
    ) -> 'CollectionConfiguration':
        collection = cls(
            config=config
        )
        collection.validate()
        return collection

    @staticmethod
    def _config_from_source(source_dict: Dict[str, Any]) -> DriverConfig:
        from monosi.drivers.factory import load_config

        if 'type' not in source_dict:
            raise Exception("Source type is required.")

        driver_type = source_dict.pop('type')
        try:
            cls = load_config(driver_type)
            data = cls.retrieve_data(source_dict)
            cls.validate(data)
            config = cls.from_dict(data)
        except Exception as e:
            raise e

        return config

    @classmethod
    def _get_source_dict(cls, collection_dict: Dict[str, Any], source_name: Optional[str]):
        if 'sources' not in collection_dict:
            raise Exception
        sources = collection_dict['sources']

        if source_name not in sources:
            raise Exception
        source_dict = sources[source_name]

        if not isinstance(source_dict, dict):
            raise Exception

        return source_dict

    @classmethod
    def _get_collection_dict(cls, collection_name: str, collections_dict: Dict[str, Any]):
        if collection_name not in collections_dict:
            raise Exception("Collection not found: {}".format(collection_name))

        collection_dict = collections_dict[collection_name]
        if not collection_dict:
            raise Exception

        return collection_dict

    def validate(self):
        pass

    @classmethod
    def from_dict(cls, collection_dict: Dict[str, Any], source_name: str = 'default') -> 'CollectionConfiguration':
        source_dict = cls._get_source_dict(collection_dict, source_name)
        config = cls._config_from_source(source_dict)

        return cls.from_driver_config(
            config=config)

    @classmethod
    def _retrieve_collections_path(cls, collections_dir):
        collections_path_selector = os.path.join(collections_dir, 'collections.y*ml')
        matches = glob.glob(collections_path_selector)

        if len(matches) != 1:
            raise Exception("There was no monosi collections configuration file.")

        collections_path = matches[0]
        return collections_path
        
    @classmethod
    def from_args(cls, collection_name='default', source_name='default', args=None) -> 'CollectionConfiguration':
        collections_path = cls._retrieve_collections_path(DEFAULT_COLLECTIONS_DIR)
        collections_dict = yaml.parse_file(collections_path)

        # Should check args for a collection name
        collection_dict = cls._get_collection_dict(collection_name, collections_dict)

        return cls.from_dict(
            collection_dict=collection_dict,
            source_name=source_name)

