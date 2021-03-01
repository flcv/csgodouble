# About

## TL;DR
**What:** A CSGO gambling bot

**When:** November(?) 2016

**Why:** Personal amusement

**How:** Python 2.7

**Development time (approx.):** 2-3 days / 6-8 hours

## Longform
The bot is a **Python 2.7** script written in 2016 that executes **automated bets** on the gambling website **CSGODouble**. The website has since officially shutdown, but a screenshot of its appearance is available; it was a **roulette wheel** style gambling site for **in-game items** for the videogame **Counter-Strike: Global Offensive**.

The bot follows the **Martingale strategy** of roulette betting, where the bet amount is doubled after each **loss**, until being reset back to the initial wager after a **win**. The bot does not use any APIs that rely on **browser manipulation**, and instead uses a novelty method of **screenshotting** the entire screen, then **scanning** it for the results of the previous spin, and then determining the new bet amount from the **subimages** of the total image it has gathered.

The bot is admittedly extremely **amateurish**, and could be vastly improved, but is **interesting** to look back on as a **relic** from 2016.
