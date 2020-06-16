from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Attachment:
    # Basic information
    item_id: int
    name: str
    description: Optional[str]
    slug: str
    image_path: Optional[str]
    is_default: bool

    # Effects
    effects: List[Dict[str, str]] = field(default_factory=list)
