# Visual Mockup of Discord Bot Interface

## Before (Plain Text)
```
You are in a cozy tavern. The fireplace crackles warmly, and the smell of ale fills the air.

Exits: north, south, upstairs
Items: Wooden Mug, Map, Rusty Key
NPCs: Bartender, Old Man, Traveling Merchant
```

User must type: `north` or `take Map`

---

## After (Rich Embeds with Buttons)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🏰 The Prancing Pony Tavern                         [Image]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ You are in a cozy tavern. The fireplace crackles warmly, and    │
│ the smell of ale fills the air.                                 │
│                                                                   │
│ ───────────────────────────────────────────────────────────────  │
│                                                                   │
│ 🚪 Exits                                                         │
│ north, south, upstairs                                           │
│                                                                   │
│ 📦 Items                                                         │
│ Wooden Mug, Map, Rusty Key                                       │
│                                                                   │
│ 👥 NPCs                                                          │
│ Bartender, Old Man, Traveling Merchant                           │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌──────────┐ ┌──────────┐ ┌──────────────┐
│ 🚪 north │ │ 🚪 south │ │ 🚪 upstairs  │
└──────────┘ └──────────┘ └──────────────┘

┌─────────────────┐ ┌──────────┐ ┌────────────────┐
│ 📦 Wooden Mug   │ │ 📦 Map   │ │ 📦 Rusty Key   │
└─────────────────┘ └──────────┘ └────────────────┘
```

User can click buttons OR type commands!

---

## Benefits

### 1. Visual Organization
- Information is structured and easy to scan
- Emojis provide quick visual identification
- Color-coded buttons (blue for exits, green for items)

### 2. Quick Actions
- One-click movement through exits
- One-click item pickup
- Reduces typing and typos

### 3. Mobile Friendly
- Buttons are easier to tap on mobile than typing
- Formatted embeds display well on small screens
- No need to switch to keyboard

### 4. Accessibility
- Clear visual hierarchy
- Consistent layout across all game events
- Ephemeral feedback messages confirm actions

---

## Button Interaction Flow

### Exit Button Click:
```
User clicks: [🚪 north]
   ↓
Bot shows: "Moving to: north" (only visible to user)
   ↓
Command sent: "north"
   ↓
Server responds with new location
   ↓
New embed with buttons displayed
```

### Item Button Click:
```
User clicks: [📦 Map]
   ↓
Bot shows: "Taking: Map" (only visible to user)
   ↓
Command sent: "take Map"
   ↓
Server responds with pickup confirmation
   ↓
New embed (possibly without that item now)
```

---

## Edge Cases Handled

### Too Many Exits/Items
- First 5 get buttons
- All are listed in embed fields
- User can still type to use ones without buttons

### No Interactive Elements
- Falls back to plain text
- No unnecessary embed overhead

### Dialogue Scenes
- Speaker name and image shown
- Dialogue text displayed prominently
- Still shows available actions

### Images
- Location images shown when entering new areas
- Speaker images shown during conversations
- Images loaded from LlamaTale resources

---

## Technical Implementation

### Discord Components Used:
- **Embed**: Rich message formatting
- **View**: Container for interactive components
- **Button**: Interactive elements with callbacks
- **ButtonStyle**: Visual styling (Primary=blue, Success=green)

### Limits Respected:
- Max 25 components per message (Discord limit)
- Max 5 exit buttons
- Max 5 item buttons
- Total ≤ 10 buttons per message

### Callback Behavior:
- Ephemeral responses (only visible to clicking user)
- Async execution
- Direct integration with LlamaTale interface
