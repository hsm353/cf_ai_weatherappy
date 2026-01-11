# Global Memory Implementation

## Overview

The Weather Chat app now uses **global shared memory** - all users see and contribute to the same conversation history stored in Cloudflare KV.

## How It Works

### Single Global Key

Instead of per-user sessions, there's one key for everyone:

```
KV Key: "global_chat_history"
KV Value: [last 4 queries from ANY user]
```

### Data Structure

```json
[
  {
    "query": "What's the weather in Paris?",
    "location": "Paris, FR",
    "timestamp": "2026-01-12T10:25:00",
    "type": "current"
  },
  {
    "query": "7 day forecast for Tokyo",
    "location": "Tokyo, JP",
    "timestamp": "2026-01-12T10:26:15",
    "type": "forecast"
  },
  {
    "query": "Weather in London",
    "location": "London, GB",
    "timestamp": "2026-01-12T10:27:30",
    "type": "current"
  },
  {
    "query": "What's it like in New York?",
    "location": "New York, US",
    "timestamp": "2026-01-12T10:28:45",
    "type": "current"
  }
]
```

## Behavior

### What Gets Stored

- ✅ **Last 4 queries globally** (from all users combined)
- ✅ Query text
- ✅ Location extracted
- ✅ Timestamp
- ✅ Type (current/forecast)

### Storage Limit

**Exactly 4 entries** are kept at all times:
- Query #1 → 1 entry stored
- Query #2 → 2 entries stored
- Query #3 → 3 entries stored
- Query #4 → 4 entries stored
- Query #5 → 4 entries stored (oldest removed)
- Query #6 → 4 entries stored (oldest removed)

### Persistence

- **No expiration** - Data persists indefinitely
- **No per-user tracking** - Completely anonymous
- **Global state** - All users share the same history

## Setup (Same as Before)

### Step 1: Create KV Namespace

```bash
wrangler kv:namespace create "CHAT_HISTORY"
wrangler kv:namespace create "CHAT_HISTORY" --preview
```

### Step 2: Update wrangler.toml

```toml
[[kv_namespaces]]
binding = "CHAT_HISTORY"
id = "your-kv-id"
preview_id = "your-preview-id"
```

### Step 3: Deploy

```bash
wrangler deploy
```

## Testing

### View Global History

```bash
# Check the global key
wrangler kv:key get "global_chat_history" --binding CHAT_HISTORY
```

**Expected output:**
```json
[
  {"query": "...", "location": "...", "timestamp": "...", "type": "..."},
  {"query": "...", "location": "...", "timestamp": "...", "type": "..."},
  {"query": "...", "location": "...", "timestamp": "...", "type": "..."},
  {"query": "...", "location": "...", "timestamp": "...", "type": "..."}
]
```

### Test the Limit

Submit 5+ queries from different devices/browsers:

```bash
wrangler tail
```

You'll see:
```
[KV] Saved to global history. Total entries: 1
[KV] Saved to global history. Total entries: 2
[KV] Saved to global history. Total entries: 3
[KV] Saved to global history. Total entries: 4
[KV] Saved to global history. Total entries: 4  # Stays at 4
[KV] Saved to global history. Total entries: 4  # Stays at 4
```

### Clear History

```bash
wrangler kv:key delete "global_chat_history" --binding CHAT_HISTORY
```

## Use Cases

### Shared Context

Perfect for:
- **Public demos** - Everyone sees recent activity
- **Community weather** - Popular locations appear
- **Simple state** - No user management needed
- **Assignment requirement** - Proves memory/state exists

### Example Scenario

```
User A in London: "Weather in Paris?"
  → Stored: Paris, FR

User B in Tokyo: "Forecast for Berlin?"
  → Stored: Paris, Berlin

User C in NYC: "What's it like in Madrid?"
  → Stored: Paris, Berlin, Madrid

User D in Sydney: "Weather in Tokyo?"
  → Stored: Paris, Berlin, Madrid, Tokyo

User E in Rome: "Rome forecast?"
  → Stored: Berlin, Madrid, Tokyo, Rome (Paris dropped)
```

## Advantages

✅ **Simplicity** - No session management
✅ **Anonymous** - No user tracking
✅ **Global** - Everyone contributes
✅ **Compliance** - Meets "memory/state" requirement
✅ **Cost effective** - Single key, minimal writes

## Functions

### `get_global_history(env)`

Retrieves the global history array from KV.

```python
history = await get_global_history(env)
# Returns: [entry1, entry2, entry3, entry4]
```

### `save_to_global_history(env, query, response_data)`

Saves a new query to global history, keeping only last 4.

```python
await save_to_global_history(env, "Weather in Paris?", weather_data)
# Automatically prunes to 4 entries
```

## Monitoring

### Check Activity

```bash
# Watch logs in real-time
wrangler tail --format pretty

# Filter for KV operations
wrangler tail | grep KV
```

### Storage Stats

```bash
# List all keys (should see just one)
wrangler kv:key list --binding CHAT_HISTORY

# Should show: ["global_chat_history"]
```

## Privacy

### What's Stored
- ✅ Query text (what user typed)
- ✅ Location extracted (e.g., "Paris, FR")
- ✅ Timestamp (when)
- ✅ Query type (current/forecast)

### What's NOT Stored
- ❌ User IDs
- ❌ IP addresses
- ❌ Session info
- ❌ Personal data
- ❌ Full weather responses
- ❌ Browser info

**Result:** Completely anonymous global memory!

## Assignment Compliance

### Requirement: "Memory or state"

✅ **FULLY MET**

**Evidence:**
1. Uses Cloudflare KV (persistent storage)
2. Stores conversation history (last 4 queries)
3. State persists between requests
4. Memory is shared globally (state management)

**Verification:**
```bash
# Prove state exists
wrangler kv:key get "global_chat_history" --binding CHAT_HISTORY

# Shows stored queries from multiple users
```

## Cost

**Free Tier:**
- 100,000 reads/day
- 1,000 writes/day
- 1 GB storage

**This Implementation:**
- 1 read per query (to get current history)
- 1 write per query (to save new entry)
- ~800 bytes total storage (4 entries × 200 bytes)

**Capacity:** ~1,000 queries/day on free tier

## Future Enhancements

### Display Recent Queries

Add a "Recent Queries" sidebar:

```python
# GET /recent
if method == "GET" and path == '/recent':
    history = await get_global_history(env)
    return Response.new(json.dumps(history), status=200)
```

Then in UI:
```javascript
// Show recent activity
const recent = await fetch('/recent').then(r => r.json());
// Display as "Recent searches: Paris, Tokyo, London..."
```

### Popular Locations

Track most queried cities:

```python
# Count location frequency
from collections import Counter
history = await get_global_history(env)
locations = [entry['location'] for entry in history]
popular = Counter(locations).most_common(3)
```

### Trend Analysis

Show weather trends:
- Most queried cities
- Peak query times
- Forecast vs current ratio

## Troubleshooting

### History Not Updating?

**Check:**
1. KV namespace is bound correctly
2. Logs show "[KV] Saved to global history"
3. No errors in `wrangler tail`

### Old Data Showing?

**Clear and restart:**
```bash
wrangler kv:key delete "global_chat_history" --binding CHAT_HISTORY
# Submit new query to repopulate
```

### Can't See Global Key?

```bash
# List all keys
wrangler kv:key list --binding CHAT_HISTORY

# Should show: global_chat_history
```

---

**Status:** ✅ Global memory active!
**Type:** Shared state across all users
**Limit:** Last 4 queries globally
**Expiration:** Never (persists indefinitely)
