from dataclasses import dataclass
from typing import Dict

from core.drivers.base import BaseDriverConfiguration

@dataclass
class Workspace:
    name: str
    integrations: Dict[str, BaseDriverConfiguration]
    send_anonymous_stats: bool = True
