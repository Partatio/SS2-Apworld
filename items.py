from typing import Dict, TypedDict
from BaseClasses import Item, ItemClassification

class SS2item(Item):
    game = "System Shock 2"

class ItemDict(TypedDict):
    id: int
    classification: ItemClassification
    count: int
    option: str


SS2items: Dict[str, ItemDict] = {
}