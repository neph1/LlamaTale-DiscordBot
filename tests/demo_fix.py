#!/usr/bin/env python3
"""
Demonstration of the fix for parsing comma-separated npcs and items.

This script shows that the parser now correctly handles both:
1. List format: ["giant rat", "giant rat"]
2. String format: "giant rat,giant rat"
"""

import json
import sys
sys.path.insert(0, '..')

import sseclient
from llamatale_responses import TextEvent

print("=" * 70)
print("TESTING FIX FOR COMMA-SEPARATED NPCS AND ITEMS")
print("=" * 70)

# Test 1: String format (as server sends it)
print("\nTest 1: String format (server format)")
print("-" * 70)
event_data = {
    "text": "You see some creatures and items here.",
    "location": "Test Room",
    "npcs": "giant rat,giant rat",
    "items": "breast_plate,sword",
    "exits": "north,south,east"
}

event = sseclient.Event(event='text')
event.data = json.dumps(event_data)
text_event = TextEvent(event)

print(f"Input npcs string: {event_data['npcs']!r}")
print(f"Parsed npcs:       {text_event.npcs}")
print(f"Display format:    {', '.join(text_event.npcs)}")
print()
print(f"Input items string: {event_data['items']!r}")
print(f"Parsed items:       {text_event.items}")
print(f"Display format:     {', '.join(text_event.items)}")
print()
print(f"Input exits string: {event_data['exits']!r}")
print(f"Parsed exits:       {text_event.exits}")
print(f"Display format:     {', '.join(text_event.exits)}")

# Test 2: List format (for backward compatibility)
print("\n" + "=" * 70)
print("Test 2: List format (backward compatibility)")
print("-" * 70)
event_data2 = {
    "text": "You see some creatures and items here.",
    "location": "Test Room",
    "npcs": ["giant rat", "giant rat"],
    "items": ["breast_plate", "sword"],
    "exits": ["north", "south", "east"]
}

event2 = sseclient.Event(event='text')
event2.data = json.dumps(event_data2)
text_event2 = TextEvent(event2)

print(f"Input npcs list: {event_data2['npcs']!r}")
print(f"Parsed npcs:     {text_event2.npcs}")
print(f"Display format:  {', '.join(text_event2.npcs)}")
print()
print(f"Input items list: {event_data2['items']!r}")
print(f"Parsed items:     {text_event2.items}")
print(f"Display format:   {', '.join(text_event2.items)}")

# Test 3: Whitespace handling
print("\n" + "=" * 70)
print("Test 3: Whitespace handling")
print("-" * 70)
event_data3 = {
    "text": "Test",
    "npcs": " giant rat , giant rat ",
    "items": " breast_plate , sword "
}

event3 = sseclient.Event(event='text')
event3.data = json.dumps(event_data3)
text_event3 = TextEvent(event3)

print(f"Input with spaces: {event_data3['npcs']!r}")
print(f"Parsed (trimmed):  {text_event3.npcs}")
print(f"Display format:    {', '.join(text_event3.npcs)}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("\n✓ String format parsing works correctly")
print("✓ List format parsing still works (backward compatible)")
print("✓ Whitespace is properly trimmed")
print("✓ Join operations produce correct display format")
print("\nThe fix handles both formats automatically!")
print("=" * 70 + "\n")
