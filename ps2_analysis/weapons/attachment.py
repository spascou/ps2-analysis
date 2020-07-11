from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ps2_analysis.fire_groups.fire_group import FireGroup


@dataclass
class Attachment:
    item_id: int
    attachment_item_id: int
    name: str
    description: str
    slug: str
    is_default: bool
    image_path: Optional[str] = None
    effects: List[Dict[str, str]] = field(default_factory=list)
    fire_groups: List[FireGroup] = field(default_factory=list)
