from typing import Dict, List, Optional


class Attachment:
    # Basic information
    item_id: int
    name: str
    description: Optional[str]
    slug: str
    image_path: Optional[str]
    is_default: bool

    # Effects
    effects: List[Dict[str, str]]

    def __init__(
        self,
        # Basic information
        item_id: int,
        name: str,
        description: Optional[str],
        slug: str,
        image_path: Optional[str],
        is_default: bool,
    ):
        # Basic information
        self.item_id = item_id
        self.name = name
        self.description = description
        self.slug = slug
        self.image_path = image_path
        self.is_default = is_default

        # Effects
        self.effects = []
