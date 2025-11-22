# Discord Bot Embed and Button Features

This document describes the expanded graphical interface features for the LlamaTale Discord bot.

## Overview

The Discord bot now leverages Discord's rich interface capabilities by using embeds and interactive buttons. This makes the game more engaging and easier to play.

## Features

### 1. Rich Embeds

When the bot receives an event with exits, items, or NPCs, it displays the information in a formatted embed with:

- **Description**: The main text/narrative from the game
- **Exits Field**: Shows all available exits with a 🚪 emoji
- **Items Field**: Shows all items in the location with a 📦 emoji
- **NPCs Field**: Shows all NPCs present with a 👥 emoji

### 2. Interactive Buttons

#### Exit Buttons
- Up to 5 exit buttons are displayed below the embed
- Each button is labeled with 🚪 and the exit name (e.g., "🚪 north")
- Clicking an exit button sends that direction as a command
- Shows an ephemeral confirmation message (only visible to you)

#### Item Buttons
- Up to 5 item buttons are displayed below the embed
- Each button is labeled with 📦 and the item name (e.g., "📦 Sword")
- Clicking an item button sends "take [item name]" as a command
- Shows an ephemeral confirmation message (only visible to you)

### 3. Location and Speaker Images

- **Location Images**: When you enter a new location, the location image is displayed in an embed
- **Speaker Images**: When an NPC speaks, their image is displayed with their dialogue

### 4. Graceful Fallback

When there are no exits or items (e.g., during pure narrative text), the bot falls back to plain text output without embeds.

## Examples

### Room with Exits and Items

```
┌─────────────────────────────────────────────┐
│  You are in a cozy tavern. The fireplace   │
│  crackles warmly, and the smell of ale     │
│  fills the air.                             │
│                                             │
│  🚪 Exits: north, south, upstairs           │
│  📦 Items: Wooden Mug, Map, Rusty Key       │
│  👥 NPCs: Bartender, Old Man, Merchant      │
└─────────────────────────────────────────────┘
[🚪 north] [🚪 south] [🚪 upstairs]
[📦 Wooden Mug] [📦 Map] [📦 Rusty Key]
```

### Treasure Room

```
┌─────────────────────────────────────────────┐
│  You've discovered a secret treasure room! │
│  Gold and jewels glitter in the torchlight.│
│                                             │
│  🚪 Exits: west                             │
│  📦 Items: Gold Coins, Ruby Amulet,         │
│           Silver Dagger, Magic Scroll,      │
│           Diamond Ring, Ancient Crown       │
└─────────────────────────────────────────────┘
[🚪 west]
[📦 Gold Coins] [📦 Ruby Amulet] [📦 Silver Dagger]
[📦 Magic Scroll] [📦 Diamond Ring]
```

## Technical Details

### Event Data Structure

The bot now fully interprets the event JSON from the LlamaTale server:

```json
{
  "text": "You are in a room.",
  "location": "Grand Hall",
  "location_image": "grand_hall.png",
  "npcs": ["King", "Guard"],
  "items": ["Crown", "Sword"],
  "exits": ["north", "south"],
  "special": []
}
```

### Button Limits

Discord has a limit of 25 components per message. The bot respects this by:
- Showing up to 5 exit buttons
- Showing up to 5 item buttons (using remaining slots after exits)
- All exits and items are still listed in the embed fields

### Changes Made

1. **llamatale.py**: Modified `_parse_event()` to pass the full `TextEvent` object through the push method
2. **discord_bot.py**: 
   - Added `GameActionView` class to handle button interactions
   - Updated `_output()` to create embeds with buttons when appropriate
   - Modified `push()` method to accept and store the event object
3. **Tests**: Added comprehensive tests for event data preservation and embed functionality

## Testing

Run the demonstration script to see examples of all features:

```bash
cd tests
python demo_embeds.py
```

Run the full test suite:

```bash
pytest tests/ -v
```

## Mock Data

See `tests/mock_data.py` for example event data structures that can be used for testing.
