# Quick Start: Using Item and NPC Icons

## For Players

When you examine an item or NPC in the game, you'll now see a small thumbnail icon in the embed!

### Example Commands:
```
examine Magic Sword
examine Guard Captain
examine Ancient Scroll
examine Wise Wizard
```

### What You'll See:
```
┌──────────────────────────────────────────────────┐
│                                [Icon appears here]│
│ Description of the item or NPC...                │
│                                                   │
│ 🚪 Exits: north, south                           │
│ 📦 Items: Magic Sword, Shield                    │
│ 👥 NPCs: Guard Captain, Merchant                 │
└──────────────────────────────────────────────────┘
```

The icon appears as a small thumbnail in the top-right corner of the embed.

## For Server Developers

### Quick Setup:

1. **Create icon images** and place them in your `tale/web/resources/` folder
2. **Name them** descriptively (e.g., `sword_legendary.png`, `guard_portrait.png`)
3. **Include in events** (optional):

```python
event = {
    "text": description,
    "location": "Armory",
    "items": ["Magic Sword", "Shield"],
    "item_images": ["sword_legendary", "shield_icon"],  # Optional!
    "npcs": ["Guard Captain"],
    "npc_images": ["captain_portrait"],  # Optional!
    "exits": ["north"]
}
```

### Supported Image Formats:
- `.png` (recommended)
- `.jpg`
- `.gif` (animated icons work!)

### Image Naming:

**Option 1: Explicit names** (provide `item_images` array)
```python
"items": ["Magic Sword"],
"item_images": ["sword_legendary"]
# Bot will look for: sword_legendary.png/jpg/gif
```

**Option 2: Auto-derived** (omit `item_images` array)
```python
"items": ["Magic Sword"]
# Bot will look for: magic_sword.png/jpg/gif
```

### Best Practices:

✅ **DO:**
- Use clear, recognizable icons (64x64 to 256x256 pixels work well)
- Keep file sizes small (< 500KB)
- Use consistent naming conventions
- Provide icons for frequently examined items/NPCs

❌ **DON'T:**
- Use huge images (Discord thumbnails are small)
- Worry if you don't have icons - the bot works fine without them
- Feel obligated to provide icons for every item

### Fallback Behavior:

If no image is found, the embed displays **without a thumbnail**. Everything else works normally!

```python
# Server sends:
"items": ["Mysterious Box"]
# No item_images provided

# Bot looks for: mysterious_box.png/jpg/gif
# If not found: Shows embed without thumbnail
# If found: Shows embed with thumbnail ✨
```

## Testing Your Icons

1. Start the Discord bot
2. Join the game with `/start`
3. Use `examine <item>` or `examine <npc>`
4. Check if the thumbnail appears
5. If not, verify:
   - Image file exists in `tale/web/resources/`
   - Image name matches (derived or explicit)
   - File format is .png, .jpg, or .gif

## Examples

### Example 1: Weapon Icons
```python
event = {
    "items": ["Steel Sword", "Iron Dagger", "Wooden Staff"],
    "item_images": ["weapon_sword", "weapon_dagger", "weapon_staff"]
}
```

Place in resources:
- `weapon_sword.png`
- `weapon_dagger.png`
- `weapon_staff.png`

### Example 2: NPC Portraits
```python
event = {
    "npcs": ["Wizard Merlin", "Guard Captain", "Shop Keeper"],
    "npc_images": ["merlin_portrait", "captain_portrait", "shopkeeper_portrait"]
}
```

Place in resources:
- `merlin_portrait.png`
- `captain_portrait.png`
- `shopkeeper_portrait.png`

### Example 3: Mixed (Some Custom, Some Auto)
```python
event = {
    "items": ["Legendary Sword", "Health Potion", "Old Key"],
    "item_images": ["sword_legendary", "", ""]  # Only first has custom icon
}
```

Bot will look for:
- `sword_legendary.png` (custom)
- `health_potion.png` (auto-derived from "Health Potion")
- `old_key.png` (auto-derived from "Old Key")

## Need Help?

- Full documentation: [ITEM_NPC_ICONS.md](ITEM_NPC_ICONS.md)
- Implementation details: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- Visual examples: [VISUAL_MOCKUP.md](VISUAL_MOCKUP.md)

## Questions?

**Q: Are icons required?**
A: No! The bot works fine without them. Icons are optional visual enhancements.

**Q: What size should icons be?**
A: 64x64 to 256x256 pixels work well. Discord will resize them automatically.

**Q: Can I use animated GIFs?**
A: Yes! .gif format is fully supported.

**Q: Do I need to restart the bot after adding images?**
A: No, images are loaded dynamically when needed.

**Q: What if the image file is missing?**
A: The embed displays normally, just without the thumbnail. No errors shown.

**Q: Can I use HTTP URLs for images?**
A: Yes, the bot supports both local files and HTTP URLs.
