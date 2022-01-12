from dataclasses import dataclass
import logging
from typing import Any, Dict, Optional, Tuple
import glob
import os
import uuid

from monosi.drivers import DriverConfig
import monosi.events as events
import monosi.utils.yaml as yaml

DEFAULT_COLLECTIONS_DIR = os.path.join(os.path.expanduser('~'), '.monosi')

def read_user_id(user_filepath: str):
    user_data = yaml.parse_file(user_filepath)
    return user_data['id']

def write_user_id(user_filepath: str):
    user_id = str(uuid.uuid4())

    if not os.path.exists(user_filepath):
        user_data = {"id": user_id}
        yaml.write_file(user_filepath, user_data)

    return user_id

def convert_to_bool(val):
    if val and val.lower() == "true":
        return True
    
    return False

@dataclass 
class CollectionConfigurationDefaults:
    collections_dir: str = DEFAULT_COLLECTIONS_DIR # TODO: Update to args
    send_anonymous_stats: bool = True

@dataclass
class CollectionConfigurationBase:
    config: DriverConfig

@dataclass
class CollectionConfiguration(CollectionConfigurationDefaults, CollectionConfigurationBase):
    @classmethod
    def from_driver_config(
        cls,
        config: DriverConfig,
        send_anonymous_stats: bool,
    ) -> 'CollectionConfiguration':
        collection = cls(
            config=config,
            send_anonymous_stats=send_anonymous_stats,
        )
        collection.validate()
        collection._initialize_events()
        return collection
    
    def _initialize_events(self):
        if not self.send_anonymous_stats:
            return

        user_filepath = os.path.join(self.collections_dir, '.cookie.yml')
        try:
            if os.path.exists(user_filepath):
                user_id = read_user_id(user_filepath)
            else:
                user_id = write_user_id(user_filepath)
            events.set_user_id(user_id)
        except:
            logging.error("There was an issue sending anonymous usage stats with a user id.")

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
            raise Exception("Source name not found")
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
        if not os.path.exists(self.collections_dir):
            raise Exception("Collections directory does not exist.")

        return True

    @classmethod
    def from_dict(cls, collection_dict: Dict[str, Any], source_name: str = 'default') -> 'CollectionConfiguration':
        source_dict = cls._get_source_dict(collection_dict, source_name)
        config = cls._config_from_source(source_dict)

        send_anonymous_stats = convert_to_bool(collection_dict['send_anonymous_stats']) if 'send_anonymous_stats' in collection_dict else True

        return cls.from_driver_config(
            config=config,
            send_anonymous_stats=send_anonymous_stats
        )

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

