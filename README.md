#Flight Game

A keyboard-controlled, text-based flight game written in Python. You start at a random airport, get a random target airport somewhere in the world, and try to reach it  but you **cannot fly straight to the target**. Each turn you only choose a direction (North, South, East or West), and the game flies you to the nearest real airport in that direction. Every flight costs money, so choose wisely!

This project was made for the **Software 1** course as a group project. It uses the course MariaDB database `flight_game` and its `airport` table.

---

## Table of contents

1. The idea
2. How to play
3. Rules, prices and scoring
4. Example game
5. How the code works
6. Settings you can change
7. Team

---

## The idea

- You start with **€1,000** at a randomly chosen airport.
- The game picks a random **target airport**.
- On each turn you choose **N, S, E or W**. The game finds the nearest airport in that direction and shows you the distance and the price.
- You can accept or cancel the flight.
- When you land **exactly** on the target airport, you complete the level, get a bonus, and receive a new target that is **farther away**.
- The game ends when your money runs out (or when you press **Q**).
- At the end you see your total distance, level reached and final score.

---

## How to play

Before every move the game shows your situation:

```
Current airport: Helsinki Vantaa Airport (EFHK)
Target airport: Sydney Kingsford Smith (YSSY)
Money: €1000
Total distance: 0 km
Level: 1   Score: 0
```

Then you type one key and press Enter:

| Key | Action |
 `N`  Fly to the nearest airport to the **north** 
 `S`  Fly to the nearest airport to the **south** 
 `E`  Fly to the nearest airport to the **east** 
 `W`  Fly to the nearest airport to the **west** 
 `Q`  Quit the game and show the final summary 

After choosing a direction you will see the destination, the distance and the price. Type `Y` to fly or `N` to cancel.

Good to know:

- Typing anything other than N, S, E, W or Q shows an error message and changes nothing.
- If there is no airport in that direction, you are told so and nothing is charged.
- If you cannot afford the flight, you get a message and stay where you are.
- A cancelled flight never changes your money, distance, position or score.

---

## Rules, prices and scoring

Starting money: €1,000
Flight price: **€0.18 per kilometre**, rounded to the nearest euro |
Minimum price  **€40** per flight 
Points for flying  Every completed flight gives points equal to the distance flown (rounded) 
Level bonus Landing on the target gives **500 × current level** points 
Next target  At least **1,000 km × new level** away from your position 
Game over  When your money reaches zero or below, or when you press `Q` 

Distances are calculated from the airports' real coordinates using **geodesic (real-world) distance**, not a straight line on a flat map.

---

## Example game

```
Welcome to Flight Adventure!

Current airport: Turku Airport (EFTU)
Target airport: Cairo International Airport (HECA)
Money: €1000
Total distance: 0 km
Level: 1   Score: 0
Choose N, S, E, W, or Q to quit: S
Destination: Tallinn Lennart Meri Airport (EETN)
Distance: 158 km
Flight price: €40
Fly there? (Y/N): Y
You landed at Tallinn Lennart Meri Airport.

Current airport: Tallinn Lennart Meri Airport (EETN)
...
Choose N, S, E, W, or Q to quit: Q

Game over.
Total distance flown: 158 km
Level reached: 1
Final score: 158
```

*(Airport names and distances in this example are illustrative.)*

---

## How the code works

Everything is in one file: `flight_game.py`. It only uses topics from the course lessons (variables, input, `if`, `while`, `for`, lists, tuples, functions and database queries).

### 1. Loading the airports (once)

At startup the program connects to the database and runs one query:

```sql
SELECT ident, name, latitude_deg, longitude_deg FROM airport
```

Airports without coordinates are removed **in Python**, and the rest are stored in a list called `kentat`. Each airport is a tuple:

```
(ident, name, latitude, longitude)
```

After this, the game never asks the database again — all lookups use the list in memory.

### 2. The functions

| Function | What it does |

| `etsi_lahin_suunnassa(kentat, nykyinen, suunta)` | Goes through the airports that lie in the chosen direction, measures the exact distance to each one with `geodesic()`, and returns the nearest airport and its distance. If nothing lies that way, the distance is `-1`. |
| `valitse_tavoite(kentat, nykyinen, minimietaisyys)` | Picks a random airport that is different from the current one and at least `minimietaisyys` km away. |

### 3. The main loop

The main program repeats these steps while the game is running and you have money:

1. Show current airport, target, money, distance, level and score.
2. Ask for a direction (N/S/E/W) or Q.
3. Find the nearest airport in that direction and calculate the price.
4. Ask to confirm the flight.
5. If confirmed: subtract the price, add distance and points, move to the new airport.
6. If you landed on the target: add the level bonus, increase the level, pick a new farther target.

### 4. What "in that direction" means

The direction is decided by comparing coordinates with your current position:

- **N** = airports with a higher latitude
- **S** = airports with a lower latitude
- **E** = airports with a higher longitude
- **W** = airports with a lower longitude

From those, the game chooses the one with the **shortest real-world distance**.

---

## Settings you can change

All game numbers are at the top of `flight_game.py`:

```python
ALKURAHA = 1000       # starting money (euros)
HINTA_KM = 0.18       # euros per kilometre
MIN_HINTA = 40        # minimum flight price (euros)
BONUS = 500           # level bonus = BONUS * level
KYNNYS_KM = 1000      # new target is at least KYNNYS_KM * level km away
```

---

## Known limitations

- **Direction rule is simple.** Because "east" just means "a higher longitude", the nearest "east" airport can sometimes lie almost due north or south of you. The map also does not wrap around at the 180° line.
- **Short pauses.** The game measures exact distances to many airports, so expect a few seconds of waiting when choosing a direction, and when a new target is picked at the start and after each level.
- **Difficulty stops growing at very high levels.** The target must be `1000 km × level` away. At around level 13 and above almost no airport is that far away, so the game falls back to any random airport.
- **Stuck with a little money.** The game only ends at €0 or below. If you have less than €40 left, no flight is affordable — press `Q` to see your final score.
- **Scoring rewards distance.** Points come from how far you fly, not from how efficient your route is. This is a known trade-off of this prototype; a future version could reward shorter routes.
- The game runs in the console only: no map, no graphics, no web interface.

---

## Team

Made by the Software 1 project group.

- Inocent

Course: Software 1 · Database: course MariaDB `flight_game`
