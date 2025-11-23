"""
Example demonstration of Discord embed and button functionality.

This script shows how the new Discord interface handles events with
exits, items, and NPCs by creating embeds with interactive buttons.
"""
import json
import sys
from unittest.mock import MagicMock

# Add parent directory to path for imports
sys.path.insert(0, '..')

import sseclient
from tests.mock_data import (
    room_with_exits_and_items,
    crossroads_location,
    treasure_room,
    dialogue_scene,
    simple_narrative,
    combat_scene
)
from llamatale_responses import TextEvent


def demonstrate_event_parsing(event_data, description):
    """Demonstrate how an event is parsed and what data is available for Discord."""
    print(f"\n{'=' * 70}")
    print(f"DEMO: {description}")
    print(f"{'=' * 70}")
    
    # Create an SSE event from mock data
    event = sseclient.Event(event='text')
    event.data = json.dumps(event_data)
    
    # Parse the event
    text_event = TextEvent(event)
    
    # Display what would be shown in Discord
    print(f"\n📝 Text Message:")
    print(f"   {text_event.text}")
    
    if text_event.location:
        print(f"\n📍 Location: {text_event.location}")
        if text_event.location_image:
            print(f"   Image: {text_event.location_image}")
    
    if text_event.speaker:
        print(f"\n💬 Speaker: {text_event.speaker}")
        print(f"   Image: {text_event.speaker_image}")
    
    # Show what would be in the embed fields
    if text_event.exits:
        print(f"\n🚪 Exits Field:")
        print(f"   {', '.join(text_event.exits)}")
        
        # Show which exits get buttons (first 5)
        button_exits = text_event.exits[:5]
        print(f"\n🔘 Exit Buttons (max 5):")
        for exit_name in button_exits:
            print(f"   [🚪 {exit_name}] -> Command: {exit_name}")
    
    if text_event.items:
        print(f"\n📦 Items Field:")
        print(f"   {', '.join(text_event.items)}")
        
        # Show which items get buttons (first 5)
        button_items = text_event.items[:5]
        print(f"\n🔘 Item Buttons (max 5):")
        for item_name in button_items:
            print(f"   [📦 {item_name}] -> Command: take {item_name}")
    
    if text_event.npcs:
        print(f"\n👥 NPCs Field:")
        print(f"   {', '.join(text_event.npcs)}")
    
    if not text_event.exits and not text_event.items:
        print(f"\n⚠️  No exits or items - using plain text output (no embed)")
    
    print(f"\n{'=' * 70}\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("DISCORD BOT - EMBED AND BUTTON DEMONSTRATION")
    print("=" * 70)
    print("\nThis demonstrates the new Discord interface features:")
    print("  • Rich embeds with location, exits, items, and NPCs")
    print("  • Interactive buttons for quick exits and item pickup")
    print("  • Visual organization with emojis and fields")
    print("  • Fallback to plain text when no interactive elements")
    
    # Demonstrate different scenarios
    demonstrate_event_parsing(
        room_with_exits_and_items,
        "Room with Exits and Items"
    )
    
    demonstrate_event_parsing(
        crossroads_location,
        "Location with Many Exits (Button Limit)"
    )
    
    demonstrate_event_parsing(
        treasure_room,
        "Treasure Room with Many Items"
    )
    
    demonstrate_event_parsing(
        dialogue_scene,
        "Dialogue Scene with Speaker"
    )
    
    demonstrate_event_parsing(
        simple_narrative,
        "Simple Narrative (Plain Text Fallback)"
    )
    
    demonstrate_event_parsing(
        combat_scene,
        "Combat Scene"
    )
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\nKey Features Implemented:")
    print("  ✓ Discord embeds for rich presentation")
    print("  ✓ Interactive buttons for exits (up to 5)")
    print("  ✓ Interactive buttons for items (up to 5)")
    print("  ✓ Visual organization with emojis (🚪, 📦, 👥)")
    print("  ✓ Location images displayed in embeds")
    print("  ✓ Speaker images for dialogue")
    print("  ✓ Graceful fallback to plain text when appropriate")
    print("\nButton Actions:")
    print("  • Exit buttons send the direction name as command")
    print("  • Item buttons send 'take <item>' command")
    print("  • Buttons show ephemeral confirmation messages")
    print("\n" + "=" * 70 + "\n")
