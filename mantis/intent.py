"""
MANTIS Intent
Structured representation of an intention
"""

from dataclasses import dataclass, field
from typing import Dict, Any
import time


@dataclass
class Intent:
    name: str
    raw: str                          
    entities: Dict[str, Any] = field(default_factory=dict)
    source: str = "unknown"
    confidence: float = 1.0
    timestamp: float = field(default_factory=time.time)