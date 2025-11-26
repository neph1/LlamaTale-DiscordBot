# Item and NPC Icons Feature

## Overview

The Discord bot supports displaying icons for items and NPCs on interactive buttons. This feature allows the LlamaTale server to send custom emojis for items and NPCs, which are always displayed on the action buttons.

## How It Works

### Server-Side Requirements

The LlamaTale server can optionally include `item_images` and `npc_images` arrays in the event data sent to the Discord bot. These can contain:

- **Discord custom emojis**: Format `<:name:id>` or `<a:name:id>` for animated
- **Unicode emojis**: Standard emoji characters like 🗡️, 🛡️, 👤
- **Image names**: For backward compatibility with file-based images

```json
{
  "text": "You are in a tavern.",
  "location": "Tavern",
  "location_image": "tavern",
  "npcs": ["Bartender", "Old Man", "Merchant"],
  "npc_images": ["<:bartender:123456789>", "👴", "<:merchant:987654321>"],
  "items": ["Wooden Mug", "Map", "Rusty Key"],
  "item_images": ["🍺", "<:map:111222333>", "🔑"],
  "exits": ["north", "south"],
  "special": []
}
```

**Important Notes:**
- The `item_images` and `npc_images` arrays are **optional**
- If provided, they should have the same length as `items` and `npcs` arrays respectively
- Custom Discord emojis require the bot to have access to the emoji (server emoji or Nitro)
- If not provided, default emojis are used (📦 for items, 👤 for NPCs)

### Client-Side Behavior

Icons are displayed on action buttons at all times:

```
┌──────────────────────────────────────────────────┐
│ You are in a cozy tavern...                      │
│                                                  │
│ 🚪 Exits: north, south                           │
│ 📦 Items: Wooden Mug, Map, Rusty Key            │
│ 👥 NPCs: Bartender, Old Man, Merchant           │
└──────────────────────────────────────────────────┘

[🚪 north] [🚪 south]
[🍺 Wooden Mug] [📜 Map] [🔑 Rusty Key]
[👴 Bartender] [👤 Old Man] [🛒 Merchant]
```

### Emoji Fallback Strategy

The bot uses a smart fallback strategy for button emojis:

1. **Discord custom emoji**: If `item_images` or `npc_images` contains Discord emoji format (`<:name:id>`), it's used directly
2. **Unicode emoji**: If the value is a Unicode emoji character, it's used as the button emoji
3. **Default emoji**: If no valid emoji is found, default emojis are used (📦 for items, 👤 for NPCs)

### Button Behavior

**Item buttons:**
- Display emoji alongside item name (Discord shows emoji before label)
- Clicking triggers "take [item]" command
- Green colored (success style)

**NPC buttons:**
- Display emoji alongside NPC name (Discord shows emoji before label)
- Clicking triggers "talk [npc]" command
- Gray colored (secondary style)

**Exit buttons:**
- Display with 🚪 emoji + direction in label
- Clicking triggers movement command
- Blue colored (primary style)

## Examples

### Example 1: Custom Discord Emojis

**Server event data:**
```json
{
  "text": "A finely crafted steel sword with intricate engravings.",
  "location": "Armory",
  "items": ["Steel Sword", "Wooden Shield"],
  "item_images": ["<:sword:123456789>", "<:shield:987654321>"],
  "npcs": ["Blacksmith"],
  "npc_images": ["<:blacksmith:555666777>"],
  "exits": ["north"]
}
```

**Discord output:**
```
[🚪 north]
[⚔️ Steel Sword] [🛡️ Wooden Shield]
[👨‍🏭 Blacksmith]
```

### Example 2: Unicode Emojis

**Server event data:**
```json
{
  "text": "An elderly wizard with a long white beard.",
  "location": "Wizard's Tower",
  "npcs": ["Wizard Merlin", "Apprentice"],
  "npc_images": ["🧙", "👨‍🎓"],
  "items": ["Magic Staff", "Spell Book"],
  "item_images": ["🪄", "📖"],
  "exits": ["down"]
}
```

**Discord output:**
```
[🚪 down]
[🪄 Magic Staff] [📖 Spell Book]
[🧙 Wizard Merlin] [👨‍🎓 Apprentice]
```

### Example 3: No Custom Emojis (Default Fallback)

**Server event data:**
```json
{
  "text": "A simple wooden bucket.",
  "location": "Well",
  "items": ["Wooden Bucket"],
  "npcs": ["Old Farmer"],
  "exits": ["north"]
}
```

**Discord output (uses default emojis):**
```
[🚪 north]
[📦 Wooden Bucket]
[👤 Old Farmer]
```

## Implementation Details

### Files Modified

1. **llamatale_responses.py**
   - Added parsing for `item_images` and `npc_images` fields
   - Added `get_item_image()` method to retrieve emoji/image for a specific item
   - Added `get_npc_image()` method to retrieve emoji/image for a specific NPC
   - Both methods return the raw emoji value for button display

2. **discord_bot.py**
   - Updated `GameActionView` to accept event data and NPCs
   - Added `_get_item_emoji()` and `_get_npc_emoji()` methods for button emojis
   - Added `_parse_emoji()` helper to handle Discord custom emoji format
   - Added NPC buttons alongside existing item buttons
   - NPC buttons trigger "talk [npc]" command

### Backward Compatibility

This feature is **fully backward compatible**:
- If the server doesn't send `item_images` or `npc_images`, default emojis are used
- All existing functionality continues to work without any changes
- Buttons work with or without custom emojis

## Usage for Server Developers

To add custom emojis for items and NPCs in your LlamaTale server:

### Option 1: Discord Custom Emojis

Upload custom emojis to your Discord server, then use their format:
```python
"item_images": ["<:sword:123456789012345678>", "<:shield:987654321098765432>"]
"npc_images": ["<:merchant:111222333444555666>"]
```

### Option 2: Unicode Emojis

Use standard Unicode emojis:
```python
"item_images": ["🗡️", "🛡️", "🔑"]
"npc_images": ["👤", "🧙", "👨‍🏭"]
```

### Option 3: No Custom Emojis

Simply don't include the arrays - default emojis will be used:
- Items: 📦
- NPCs: 👤

## Future Enhancements

Possible future improvements:
- Support for animated Discord emojis (already supported with `<a:name:id>` format)
- Item icons in inventory listings
- NPC portraits in dialogue embeds
