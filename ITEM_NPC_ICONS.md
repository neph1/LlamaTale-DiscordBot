# Item and NPC Icons Feature

## Overview

The Discord bot now supports displaying icons/thumbnails for items and NPCs in embeds. This feature allows the LlamaTale server to send custom images for items and NPCs, which are displayed when examining these objects.

## How It Works

### Server-Side Requirements

The LlamaTale server can optionally include `item_images` and `npc_images` arrays in the event data sent to the Discord bot:

```json
{
  "text": "You are in a tavern.",
  "location": "Tavern",
  "location_image": "tavern",
  "npcs": ["Bartender", "Old Man", "Merchant"],
  "npc_images": ["bartender_portrait", "old_man_portrait", "merchant_portrait"],
  "items": ["Wooden Mug", "Map", "Rusty Key"],
  "item_images": ["mug_icon", "map_icon", "key_icon"],
  "exits": ["north", "south"],
  "special": []
}
```

**Important Notes:**
- The `item_images` and `npc_images` arrays are **optional**
- If provided, they should have the same length as `items` and `npcs` arrays respectively
- Each image name should match the base name of an image file (without extension) in the resources folder
- If not provided, the bot will derive image names from the item/NPC names (lowercase with underscores)

### Client-Side Behavior

When a player examines an item or NPC:

```
User types: "examine Map"
   ↓
Bot tracks the command
   ↓
Server responds with item description
   ↓
Bot finds "Map" in the items list
   ↓
Bot retrieves image name: "map_icon" (from item_images) or "map" (derived)
   ↓
Bot displays description embed with thumbnail
```

### Image Fallback Strategy

The bot uses a smart fallback strategy for finding images:

1. **Explicit images**: If the server provides `item_images` or `npc_images`, use the corresponding image name
2. **Derived names**: If no explicit image is provided, derive the name from the item/NPC name:
   - Convert to lowercase
   - Replace spaces with underscores
   - Example: "Magic Sword" → "magic_sword"

### Display Behavior

**When examining an item:**
- The item's description is shown in an embed
- A thumbnail of the item appears in the top-right corner of the embed
- If the image file exists, it's loaded from the LlamaTale resources folder
- If the image file doesn't exist, no thumbnail is shown (graceful fallback)

**When examining an NPC:**
- The NPC's description is shown in an embed
- A thumbnail of the NPC appears in the top-right corner of the embed
- If the image file exists, it's loaded from the LlamaTale resources folder
- If the image file doesn't exist, no thumbnail is shown (graceful fallback)

## Examples

### Example 1: Examining an Item with Custom Icon

**Server event data:**
```json
{
  "text": "A finely crafted steel sword with intricate engravings.",
  "location": "Armory",
  "items": ["Steel Sword", "Wooden Shield"],
  "item_images": ["sword_legendary", "shield_basic"],
  "npcs": [],
  "exits": ["north"]
}
```

**User command:** `examine Steel Sword`

**Discord output:**
```
┌─────────────────────────────────────────────────────────┐
│                                          [Sword Icon]   │
│ A finely crafted steel sword with intricate            │
│ engravings.                                             │
│                                                         │
│ 🚪 Exits: north                                         │
│ 📦 Items: Steel Sword, Wooden Shield                   │
└─────────────────────────────────────────────────────────┘
```

### Example 2: Examining an NPC with Portrait

**Server event data:**
```json
{
  "text": "An elderly wizard with a long white beard and piercing blue eyes.",
  "location": "Wizard's Tower",
  "npcs": ["Wizard Merlin", "Apprentice"],
  "npc_images": ["merlin_portrait", "apprentice_portrait"],
  "items": [],
  "exits": ["down"]
}
```

**User command:** `examine Wizard Merlin`

**Discord output:**
```
┌─────────────────────────────────────────────────────────┐
│                                      [Merlin Portrait]  │
│ An elderly wizard with a long white beard and           │
│ piercing blue eyes.                                     │
│                                                         │
│ 🚪 Exits: down                                          │
│ 👥 NPCs: Wizard Merlin, Apprentice                     │
└─────────────────────────────────────────────────────────┘
```

### Example 3: No Custom Images (Fallback)

**Server event data:**
```json
{
  "text": "A simple wooden bucket.",
  "location": "Well",
  "items": ["Wooden Bucket"],
  "npcs": [],
  "exits": ["north"]
}
```

**User command:** `examine Wooden Bucket`

The bot will look for an image file named `wooden_bucket.png`, `wooden_bucket.jpg`, or `wooden_bucket.gif` in the resources folder. If found, it displays it. If not found, the embed is shown without a thumbnail.

## Implementation Details

### Files Modified

1. **llamatale_responses.py**
   - Added parsing for `item_images` and `npc_images` fields
   - Added `get_item_image()` method to retrieve image name for a specific item
   - Added `get_npc_image()` method to retrieve image name for a specific NPC
   - Both methods implement fallback to derived names

2. **discord_bot.py**
   - Added `last_command` tracking to detect examine commands
   - Updated `_output()` method to add thumbnails when examining items/NPCs
   - Integrated with existing embed system
   - Handles both HTTP URLs and local file paths for images

### Backward Compatibility

This feature is **fully backward compatible**:
- If the server doesn't send `item_images` or `npc_images`, the bot uses derived names
- If image files don't exist, embeds are displayed without thumbnails
- All existing functionality continues to work without any changes

### Resource Management

The bot uses the same resource loading mechanism as location and speaker images:
- Images are loaded from the LlamaTale resources folder
- Supports `.png`, `.jpg`, and `.gif` formats
- Can load from local paths or HTTP URLs
- Caches resources according to Discord's file handling

## Testing

Run the test suite to verify functionality:

```bash
pytest tests/test_llamatale_responses.py -v
```

Tests cover:
- Parsing `item_images` and `npc_images` from server events
- Image retrieval for specific items and NPCs
- Fallback to derived names when explicit images aren't provided
- Handling of missing or incomplete image arrays

## Usage for Server Developers

To add custom icons for items and NPCs in your LlamaTale server:

1. Create icon images and place them in the `tale/web/resources/` folder
2. Name them descriptively (e.g., `sword_legendary.png`, `merchant_portrait.png`)
3. Include `item_images` and/or `npc_images` arrays in your event data
4. Ensure arrays match the length and order of `items` and `npcs` arrays

**Example event structure:**
```python
event = {
    "text": description,
    "location": location_name,
    "location_image": location_image_name,
    "npcs": [npc1.name, npc2.name],
    "npc_images": [npc1.icon, npc2.icon],  # Optional
    "items": [item1.name, item2.name],
    "item_images": [item1.icon, item2.icon],  # Optional
    "exits": exit_names,
    "special": special_items
}
```

## Future Enhancements

Possible future improvements:
- Display item icons in inventory listings
- Show NPC portraits in dialogue embeds
- Add hover tooltips with item/NPC stats
- Support animated icons (GIF format already supported)
- Thumbnail galleries for locations with many items
