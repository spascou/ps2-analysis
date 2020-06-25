from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ps2_analysis.fire_groups.fire_group import FireGroup


@dataclass
class Attachment:
    # Basic information
    item_id: int
    attachment_item_id: int
    name: str
    description: Optional[str]
    slug: str
    image_path: Optional[str]
    is_default: bool

    # Effects
    effects: List[Dict[str, str]] = field(default_factory=list)

    # Fire groups
    fire_groups: List[FireGroup] = field(default_factory=list)
