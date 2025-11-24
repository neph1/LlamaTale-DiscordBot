"""
Mock data examples for testing Discord bot with embeds and buttons.

This file contains example event data that the LlamaTale server might send,
demonstrating the expanded interface with exits, items, and NPCs.

NOTE: The server can send npcs, items, and exits in two formats:
1. As lists: ["item1", "item2"]
2. As comma-separated strings: "item1,item2"
The parser handles both formats automatically.
"""

# Example 1: A room with exits and items (list format)
room_with_exits_and_items = {
    "text": "You are in a cozy tavern. The fireplace crackles warmly, and the smell of ale fills the air.",
    "location": "The Prancing Pony Tavern",
    "location_image": "tavern",
    "npcs": ["Bartender", "Old Man", "Traveling Merchant"],
    "npc_images": ["bartender_portrait", "old_man_portrait", "merchant_portrait"],
    "items": ["Wooden Mug", "Map", "Rusty Key"],
    "item_images": ["mug_icon", "map_icon", "key_icon"],
    "exits": ["north", "south", "upstairs"],
    "special": []
}

# Example 2: A location with many exits (testing button limits)
crossroads_location = {
    "text": "You stand at a busy crossroads. Paths lead in all directions.",
    "location": "The Crossroads",
    "location_image": "crossroads",
    "npcs": ["Guard"],
    "items": ["Signpost"],
    "exits": ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"],
    "special": []
}

# Example 3: A treasure room with many items
treasure_room = {
    "text": "You've discovered a secret treasure room! Gold and jewels glitter in the torchlight.",
    "location": "Secret Treasure Vault",
    "location_image": "treasure_vault",
    "npcs": [],
    "npc_images": [],
    "items": ["Gold Coins", "Ruby Amulet", "Silver Dagger", "Magic Scroll", "Diamond Ring", "Ancient Crown"],
    "item_images": ["coins_icon", "amulet_icon", "dagger_icon", "scroll_icon", "ring_icon", "crown_icon"],
    "exits": ["west"],
    "special": ["chest"]
}

# Example 4: A dialogue scene with NPCs
dialogue_scene = {
    "text": "The wizard <:> Greetings, traveler! I sense great potential in you.",
    "location": "Wizard's Tower",
    "location_image": "wizard_tower",
    "npcs": ["Wizard Merlin", "Apprentice"],
    "items": ["Spell Book", "Crystal Ball"],
    "exits": ["down"],
    "special": []
}

# Example 5: Simple text without exits or items (fallback to plain text)
simple_narrative = {
    "text": "You walk down the path. The sun is setting, casting long shadows.",
    "location": None,
    "location_image": None,
    "npcs": [],
    "items": [],
    "exits": [],
    "special": []
}

# Example 6: Combat scenario
combat_scene = {
    "text": "A goblin jumps out from behind a rock!",
    "location": "Mountain Path",
    "location_image": "mountain_path",
    "npcs": ["Goblin Warrior"],
    "items": ["Rock", "Broken Sword"],
    "exits": ["north", "south"],
    "special": ["combat"]
}

# Example 7: String format (as the server actually sends)
string_format_example = {
    "text": "You see some creatures and items here.",
    "location": "Test Room",
    "location_image": "test_room",
    "npcs": "giant rat,giant rat",
    "items": "breast_plate,sword",
    "exits": "north,south,east",
    "special": ""
}

# Usage example for testing:
"""
To test these examples in the actual Discord bot, you would:

1. Mock the SSE event stream from LlamaTale server
2. Convert the dictionary to JSON and wrap in an sseclient.Event
3. Pass to the _parse_event method

Example test code:
```python
import json
import sseclient
from llamatale import LlamaTaleInterface

# Create event from mock data
event = sseclient.Event(event='text')
event.data = json.dumps(room_with_exits_and_items)

# Process the event
llama_tale_interface = LlamaTaleInterface(config)
llama_tale_interface._parse_event(event)
```

Expected Discord UI behavior:
- For room_with_exits_and_items: 
  * Embed with the text description
  * Fields showing: 🚪 Exits: north, south, upstairs
  * Fields showing: 📦 Items: Wooden Mug, Map, Rusty Key  
  * Fields showing: 👥 NPCs: Bartender, Old Man, Traveling Merchant
  * Buttons: "🚪 north", "🚪 south", "🚪 upstairs"
  * Buttons: "📦 Wooden Mug", "📦 Map", "📦 Rusty Key"

- For crossroads_location:
  * Shows exits up to Discord's limit (first 5 exits get buttons)
  * Remaining exits still listed in the embed field

- For treasure_room:
  * Shows item buttons up to Discord's limit (first 5 items)
  * All items listed in embed field

- For dialogue_scene:
  * Shows speaker name and image
  * Provides interaction buttons

- For simple_narrative:
  * Falls back to plain text output (no embed)
  * No buttons since no exits or items
"""
