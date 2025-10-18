# Beeline - Testing Guide

## 🧪 Mock Routes Available for Testing

I've created **4 different mock route scenarios** that you can test right now without any backend!

### Test Queries:

#### 1. **San Jose to Salesforce Tower** (Default - 3 routes)
```
Get me from San Jose to Salesforce Tower by 10 am
```
**What you'll see:**
- Route 1: Drive to Millbrae, Caltrain (75 min, $18.50) ⭐ Fastest
- Route 2: Drive to Mountain View, Caltrain Express (82 min, $14.25) 💰 Cheapest
- Route 3: Drive to Daly City BART, BART to SF (85 min, $14.20)

**Features to test:**
- 🚗 Drive segments (blue lines)
- 🅿️ Parking at stations (purple markers)
- 🚆 Transit (red lines - Caltrain & BART)
- 🚶 Walking (green lines)

---

#### 2. **Palo Alto to Oracle Park** (Transit-only - 1 route)
```
Palo Alto to Oracle Park by 7pm
```
or
```
I'm in Palo Alto. Need to get to Oracle Park. Don't want to pay for parking.
```

**What you'll see:**
- Route 1: Walk → Caltrain → Walk (68 min, $8.75) 🌱 Greenest

**Features to test:**
- Transit-only route (no driving/parking)
- Lower cost
- High carbon savings (12.4 kg CO₂)
- High confidence (95%)

---

#### 3. **Milpitas to Moscone Center** (Mix of modes - 3 routes)
```
Get me from Milpitas to Moscone Center by 11am
```
or
```
Milpitas to Moscone. I'm okay with Uber or BART.
```

**What you'll see:**
- Route 1: Drive to Warm Springs BART → BART (62 min, $11.75) ⚡ Fastest
- Route 2: 🚕 Uber to Fremont BART → BART (58 min, $22.45) - Rideshare option!
- Route 3: Drive to Milpitas BART → BART (68 min, $9.95) 💰 Cheapest

**Features to test:**
- 🚕 Rideshare leg (Uber - orange)
- Multiple BART stations
- Different cost/time tradeoffs
- Parking availability indicators

---

#### 4. **Berkeley to Downtown Oakland** (Short trip - 3 routes)
```
Berkeley to downtown Oakland by 2pm
```
or
```
I need to get from Berkeley to Oakland. Show me all options.
```

**What you'll see:**
- Route 1: BART Downtown Berkeley → 12th St (18 min, $2.50) ⚡ Super fast
- Route 2: AC Transit Bus 51 (32 min, $2.25) 💰 Cheapest
- Route 3: 🚴 Bay Wheels bike share (28 min, $3.50) 🌱 Most eco-friendly

**Features to test:**
- 🚴 Bike mode (cyan lines)
- Short routes (under 30 min)
- Bus transit (AC Transit)
- Very high confidence (97%)

---

## 🎯 What to Test

### 1. **Basic Navigation**
- [ ] Enter a query on landing page
- [ ] See loading animation
- [ ] Results page opens with map + timeline
- [ ] 3 routes appear in left sidebar

### 2. **Route Selection**
- [ ] Click different route preview cards
- [ ] Map updates to show that route
- [ ] Timeline updates with step-by-step details
- [ ] Selected route highlights in sidebar

### 3. **Quick Filters** (Top of sidebar)
- [ ] Click "⚡ Fastest" → routes re-sort by time
- [ ] Click "💰 Cheapest" → routes re-sort by cost
- [ ] Click "🌱 Greenest" → routes re-sort by CO₂ savings

### 4. **Mode Filters** (Sidebar checkboxes)
- [ ] Uncheck "Driving" → routes with driving disappear
- [ ] Uncheck "Transit" → only driving routes remain
- [ ] Uncheck "Walking" → (most routes need walking!)
- [ ] Toggle rideshare (only shows on Milpitas routes)

### 5. **Timeline Details**
- [ ] See times for each step (8:45am, 9:20am, etc.)
- [ ] See colored icons for each mode
- [ ] See costs per leg
- [ ] See parking availability percentages
- [ ] See transit line names & stop counts

### 6. **Map Visualization**
- [ ] See colored route lines (blue, red, green, etc.)
- [ ] See markers at start (green), stops, end (red)
- [ ] Click markers to see popups
- [ ] Map auto-zooms to fit route

### 7. **Dark Mode** 🌙
- [ ] Click moon icon in header
- [ ] Entire app switches to dark theme
- [ ] Sidebar becomes darker slate
- [ ] Map stays visible
- [ ] Refresh page → theme persists
- [ ] Click sun icon → back to light mode

### 8. **Responsive Behavior**
- [ ] Sidebar stays at 25% width
- [ ] Map takes 60% of right side
- [ ] Timeline takes 40% of right side
- [ ] Scroll timeline if needed

---

## 🐛 Known Limitations (Mock Mode)

These are expected since you're using mock data:

- ❌ Queries don't affect results (only keywords matter)
- ❌ Filters work, but don't generate new routes
- ❌ Times are fixed (always shows Oct 18, 2025)
- ❌ Can't actually "select" a route (just alerts)

These will work once backend is connected!

---

## 🎨 Visual Features to Admire

### **Timeline Component**
- ✅ Clean step-by-step layout
- ✅ Exact times for each leg
- ✅ Color-coded mode icons
- ✅ Hover effects on steps
- ✅ Green "Arrive" badge at end

### **Route Preview Cards**
- ✅ Emoji mode indicators (🚗🅿️🚆🚶)
- ✅ Quick stats (time, cost, CO₂)
- ✅ Confidence badges (90%+)
- ✅ Highlight when selected

### **Dark Mode**
- ✅ Smooth transitions
- ✅ Slate sidebar (#1e293b)
- ✅ Cyan accents
- ✅ Readable everywhere

### **Map**
- ✅ OpenStreetMap (free!)
- ✅ Multi-colored route segments
- ✅ Custom markers
- ✅ Auto-zoom to route

---

## 🚀 Quick Start

```bash
cd frontend
npm run dev
```

Open http://localhost:5173

Make sure `PUBLIC_MOCK_MODE=true` in your `.env`!

---

## 💡 Demo Tips

### For judges/viewers:

1. **Start with Berkeley→Oakland** (shortest, most impressive)
   - Shows all 3 modes (BART, Bus, Bike)
   - Super fast (18 min)
   - Easy to understand

2. **Then show San Jose→SF** (classic commute)
   - Multiple Caltrain options
   - Parking visualization
   - Time/cost tradeoffs

3. **Highlight dark mode** 🌙
   - Toggle mid-demo
   - Shows polish

4. **Show filters in action**
   - Click "Fastest" → "Cheapest"
   - Uncheck "Transit" → routes disappear
   - Toggle back → routes reappear

5. **Click through route previews**
   - Show map updating
   - Timeline changing
   - Different mode combinations

---

## 🎬 Demo Script (30 seconds)

> "Beeline solves the Bay Area commute problem. Watch this:
>
> [Type: "Berkeley to Oakland by 2pm"]
>
> Instant results! Three options: BART in 18 minutes, bus, or bike share.
>
> [Click "Fastest" button]
>
> Routes re-sort instantly.
>
> [Click Route 2]
>
> See the full timeline—exact times, costs, everything.
>
> [Toggle dark mode]
>
> Oh, and it has dark mode!
>
> [Click different route]
>
> Every route visualized on the map. This is what multi-modal transit should be."

---

## Test All 4 Scenarios! 🎉

1. ✅ "San Jose to Salesforce Tower by 10am"
2. ✅ "Palo Alto to Oracle Park"
3. ✅ "Milpitas to Moscone Center"
4. ✅ "Berkeley to downtown Oakland"

Each shows different combinations of:
- 🚗 Driving
- 🅿️ Parking
- 🚆 Transit (Caltrain, BART, AC Transit)
- 🚕 Rideshare (Uber)
- 🚴 Bike share
- 🚶 Walking

**Have fun testing!** 🐝
