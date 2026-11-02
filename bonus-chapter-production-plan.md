# Bonus Chapter Channel: Production Plan (8 topics)

Covers: format split, fact-check, vidIQ keyword and title research, and scripts or outlines.
Fact-check status: **OK** = sources agree. **CAUTION** = say it carefully. **UNVERIFIED** = do not state as fact until checked.

---

## 1. Shorts vs long-form split

| # | Topic | Format | Reason |
|---|-------|--------|--------|
| 1 | Eggs: US fridge vs UK shelf | **Long (8-10 min)** + 45s Short cut | Debate topic. Needs room for washing, cuticle, vaccination and the comment-bait ending |
| 2 | What if Yellowstone erupted | **Long (10-12 min)** + Short | Needs a timeline and an ash map |
| 3 | School bus yellow | **Short** (45-55s), optional 5-min long | One surprising story: the 1939 conference |
| 4 | Why 911 | **Long (6-8 min)** + Short | A people-and-places story: Haleyville, AT&T, the FCC |
| 5 | 1-km asteroid hits NYC | **Long (10-12 min)** + Short | Visual spectacle, hour-by-hour structure |
| 6 | AMBULANCE backwards | **Short only** (30-40s) | A single reveal. Padding would hurt it |
| 7 | Cascadia | **Long (10-12 min)** + Short | Emotional and regional. Needs the real numbers |
| 8 | Stop sign octagons | **Short only** (35-45s) | Single payoff, **but see the fact-check caution** |

**Cadence:** 3 Shorts + 5 longs. Publish a Short a few days before its long-form sibling as a teaser, and end the Short with "full story on the channel".
**Suggested order (by search demand and shareability):** 2 Yellowstone, 1 Eggs, 5 Asteroid, 7 Cascadia, 4 911, then Shorts 3, 6 and 8 as fillers between longs.

---

## 2. Fact-check

### 1. Eggs: **OK, with caution on causes**
- US: USDA requires commercial eggs to be washed. Washing removes the cuticle (bloom), so refrigeration is the safeguard.
- UK/EU: eggs are not washed. The cuticle stays on, and hens are vaccinated against Salmonella.
- The US did not mandate hen vaccination. The FDA said in 2004 that more data was needed. Some US farms vaccinate voluntarily.
- Supply-chain history (no cold chain in the past) is a plausible extra reason, not the main one. Say "one explanation".
- **CAUTION:** The UK "14,000 to 8,000 cases" figure came from one blog. Do not use it without a primary source (UK FSA or UKHSA).
- **To verify before recording:** current USDA/FDA wording, and the UK Lion Code (vaccination scheme) start year.

### 2. Yellowstone: **OK**
- The 2014 USGS Ash3d study (Mastin, Van Eaton and Lowenstern) found: centimeters to over a meter of ash within about 500 km, millimeters reaching NYC, LA and Miami. Results depend on wind.
- Past caldera-forming eruptions: 2.1 million, 1.3 million and 640,000 years ago.
- USGS says a supereruption is exceedingly unlikely in any given century or millennium. **UNVERIFIED:** annual odds such as "1 in 730,000". Do not quote them. Say "exceedingly low" and cite USGS.
- Far likelier events: hydrothermal explosions and lava flows. Alert level is Normal.
- Framing note: "erupted" in the topic is ambiguous. Pick the supereruption scenario and state that it is the rare worst case.

### 3. School bus yellow: **OK**
- April 1939 conference at Teachers College, Columbia, organized by Frank W. Cyr. Rockefeller Foundation funded (about $5,000 per one source; amounts differ).
- It set the first national school-bus standards (the count of 42, 44 or other figures differs by source, so say "dozens of standards").
- Cyr displayed shades of yellow to orange. The chosen color was "National School Bus Chrome", now "National School Bus Glossy Yellow".
- Reason: visibility and contrast with black lettering. Cyr reportedly thought it was closer to orange.
- Minnesota was the last holdout (1974 per one source).
- **Peripheral vision claim (checked):** the "yellow is seen 1.24x better than red in peripheral vision" figure is widely repeated but no original study was found, and it is not tied to the 1939 conference. **Leave it out.** The safe reason is "visibility and contrast with black lettering".

### 4. 911: **OK on dates, CAUTION on "why 911"**
- 1967: the President's Commission on Law Enforcement recommended one national number. One source attributes the FCC referral to a different commission, so avoid naming which commission referred it.
- Jan 12, 1968: AT&T announced 911 (Bell system only).
- Feb 16, 1968: first call, Haleyville, Alabama (Alabama Telephone Co., an independent). Rankin Fite called Tom Bevill. It was a ceremonial call, **not a real emergency**.
- Other early cities: Nome, Alaska (Feb 22, 1968) and Huntington, Indiana (Mar 1, 1968, AT&T's first).
- **Reasons for 911 (second check):** secondary sources agree it was short, easy to remember, and unused as an area, exchange or service code. Use those, worded as "chosen because" only with a hedge ("according to NENA's account"). **Do NOT use any rotary-dial claim:** sources contradict each other. No primary AT&T/FCC document found.
- Also verify: how many Haleyville days or weeks the setup took (sources say "under a week" and "five weeks").

### 5. Asteroid hits New York: **model results, with stated limits**
- Sandia modeled a roughly 1.4 km asteroid hitting the ocean. It vaporizes, throws up water vapor and debris, and the shock wave levels much of New England.
- The crater, blast radius and casualty figures found in this pass were from consumer simulators and a fictional NASA tabletop. **Do not script numbers from them.**
- **Status (updated):** the web calculator is still unreachable, but the Collins, Melosh and Marcus (2005) paper was supplied and its equations are implemented in `asteroid_impact_model.py`, validated against the paper's Table 6. Results (1 km stony, 45 deg, 17 km/s, bedrock): about 54,000 Mt, final crater about 14 km, magnitude about 7.8, fireball radius about 12 km. See `longform-scripts-eggs-911-asteroid.md` for rings and caveats (blast likely overestimated 2-5x above about 10,000 Mt; no tsunami model; no global effects).
- **Own estimate (Collins et al. 2005 scaling equations, implemented by me, NOT the online calculator):** 1 km stony asteroid (3,000 kg/m3), 45 degrees, land target (2,500 kg/m3):

| Impact speed | Energy | Final crater | Seismic magnitude (approx.) |
|---|---|---|---|
| 12 km/s | about 27,000 Mt TNT | about 12 km | about 7.6 |
| 17 km/s | about 54,000 Mt | about 14.5 km | about 7.8 |
| 20 km/s | about 75,000 Mt | about 16 km | about 7.9 |

  The crater agrees with the roughly 12 km figure in the French Asteroid Launcher report. **Before it goes in a script:** rerun the same inputs in the Imperial/Purdue Earth Impact Effects Program and use its crater, fireball, thermal, overpressure and seismic distances (I did not compute those). The New York site is coastal, so decide land vs ocean. An ocean impact adds a tsunami and changes the crater.
- **Safe to use now:** Sandia's modeling (about 1.4 km, off the coast): the asteroid vaporizes, hundreds of cubic miles of water vapor, melted rock and debris go into the upper atmosphere, and the shock wave levels much of New England.
- **DART (checked):** 2022, Dimorphos's orbit shortened from 11 h 55 min to about 11 h 23 min (about 32-33 min; mission needed only 73 seconds). Researchers stress warning time (years) is the key.
- **"95% cataloged" (checked, soft):** a search summary of a NASA August 2025 snapshot gave 874 discovered near-Earth asteroids over 1 km with about 50 estimated still undiscovered. That is about 94-95%, but the percentage is a calculation from those two numbers, not a NASA statement, and I could not open the NASA CNEOS page. **Script: "NASA says it has found the large majority of near-Earth asteroids this size, and none is known to threaten Earth."**

---

### 6. AMBULANCE backwards: **OK on the reason, UNVERIFIED on origin**
- Mirror reversal makes the word readable in a driver's rearview mirror. This is well documented and consistent.
- The origin and date of the practice are unclear (early vs mid-20th century). **Do not name an inventor, a year or a place.** Say "common practice, exact origin unclear".
- Bonus hook that is safe: the word is mirror-flipped, but the sirens and lights make the same point: the signal is for the driver ahead.
- **To verify if used:** the "Star of Life" and "emergency vehicles also use reversed words in some other countries" claims.

### 7. Cascadia: **OK**
- USGS 2025 fact sheet: roughly 10-15% chance of a magnitude ~9 full-margin rupture in the next 50 years (about 10% time-independent, about 15% accounting for the 1700 event). The 1-in-3 figure from older work (Oregon State, 2010) covers a broader class of large quakes, so do not mix them up.
- Last full rupture: January 1700 (also recorded in Japanese "orphan tsunami" records). Recurrence about 500 years on average, with a wide spread.
- **Checked this round (secondary sources; no primary report opened):**
  - **Shaking:** 2013 DOGAMI slides say 3-5 minutes. A newer DOGAMI release says "several minutes". Script: "several minutes (DOGAMI has said 3-5)".
  - **Tsunami arrival on the Oregon coast:** sources conflict: 10-30 min (newer DOGAMI release), 15-20 min (2013 DOGAMI slides), "as early as 15 min" (2004 PNSN), about 20 min (OSU Extension). **Script: "roughly 10 to 30 minutes after shaking begins, depending on where you are."** Do not give one number.
  - **Fault length:** NOAA says about 700 miles (1,100 km), Cape Mendocino to northern Vancouver Island. The 1700 rupture is quoted at about 620 miles. Other sites say 1,000 km. Use NOAA's 700 miles and say "about".
  - **1700 event:** the wave hit Japan's Honshu coast around midnight on Jan 26-27, 1700 (sources say Jan 27 local time), 6-10 ft high, with no shaking felt, hence "orphan tsunami". Estimated magnitude about 9.0. NOAA: more than 40 quakes above M8 along the zone in the past 10,000 years.
  - **Oregon Resilience Plan (Feb 2013), checked against the primary Executive Summary (user-supplied PDF):** fatalities "from 1,250 to more than 10,000" (shaking and tsunami combined); tens of thousands of buildings destroyed or damaged; more than $30 billion direct and indirect losses (close to one-fifth of Oregon's GSP); more than one million dump-truck loads of debris. Recovery under 2013 conditions: electricity 1-3 months (valley), 3-6 months (coast); water/sewer 1 month to 1 year (valley), 1-3 years (coast); healthcare 18 months (valley), 3 years (coast); some outages 18-36 months or more. The plan recommends preparing for a minimum of two weeks, and possibly more, instead of 72 hours. **Correction:** my earlier note calling "10,000" wrong was itself mistaken (it relied on search summaries that cited "7,800 deaths and injuries"); use the plan's range. Oregon gets almost 100% of its liquid fuel from Washington. The "can't get fuel until bridges are fixed" quote is from a 2019 ODOT presentation (secondary), not the plan.
  - **ShakeAlert:** nothing found this round. Check USGS before including it.
  - **STILL OPEN:** the plan's original executive summary was not opened. Read it before quoting any casualty or cost number.

### 8. Stop signs: **CAUTION, the payoff is unconfirmed**
- William Phelps Eno is credited with the concept (1900 article, per one source). Michigan used early stop signs around 1914-1915 (sources differ on year). The 1922 AASHO committee standardized the octagon.
- Original signs were yellow, because fade-resistant red was not available. Red came later.
- The planned payoff ("recognizable from behind") was **not confirmed by any source found**. The sources point to a different reason: a distinct shape that is identifiable at night, when signs were not reflective. Rear-lit signs showing the shape is a related note.
- **DECIDED: the "from behind" claim is dropped.** The Short leads only with the sourced story (yellow first, 1922 octagon, a shape readable at night).

---

## 3. vidIQ research

### Keyword demand (US seed, vidIQ "research" mode)
| # | Seed keyword | Monthly est. | Competition | Read |
|---|--------------|-------------|-------------|------|
| 1 | why are american eggs refrigerated | <750 | 84 | Tiny, hard. Target the variant **"why americans refrigerate eggs"** (about 9,300/mo, comp 57) |
| 2 | what if yellowstone erupted | about 10,000 (+183%) | 47 | **Best.** Related: yellowstone eruption 22.5K, yellowstone supervolcano 49K (+181%), supervolcano 29K (+83%) |
| 3 | why are school buses yellow | about 3,600 | 62 | Target **"why school buses are yellow"** (about 7,800, +82%). Related: school bus history 3.8K, comp 29 |
| 4 | why is 911 the emergency number | <750 | 42 | Low direct demand. Ride "911" (343K, but falling -48%), "american history" and "police history" (15.7K, +27%) |
| 5 | asteroid hits new york | <750 | 45 | Low direct demand. Related "asteroid impact" about 6,100 (+76%). Needs a strong thumbnail more than SEO |
| 6 | why is ambulance written backwards | <750 | **25** | Low competition. Use Shorts tags ("did you know" 369K, "educational shorts" 68K, "mirror writing") |
| 7 | cascadia earthquake | about 38,800 (+447%) | 60 | **Strong, fast-rising.** Related: cascadia 46K (+101%), subduction zone 15.5K, megaquake 12.7K, tsunami 4.4K (comp 28) |
| 8 | why are stop signs octagons | <750 | **27** | Low competition. "stop sign" 52K (+28%). Shorts discovery, not search |

**Takeaways**
- Search-led longs: **Cascadia** and **Yellowstone** (high demand, rising).
- Browse/suggested-led: eggs, asteroid, 911 (low search volume, so packaging matters more).
- Shorts (3, 6, 8) run on feed discovery: use broad tags (did you know, interesting facts, american history).
- Pattern: "Why Americans..." phrasing out-searches "Why are American..." for eggs.
- vidIQ flags "what if" as a very large keyword (6.9M monthly, +147%).

### Title scores (vidIQ CTR score, 0-100)
| # | Working title | Type | Score |
|---|---------------|------|-------|
| 1 | Why Americans Refrigerate Eggs (and Brits Don't) | long | **90** |
| 2 | What If Yellowstone Erupted Tomorrow? | long | 82 |
| 3 | Why School Buses Are That Exact Yellow | long | 85 |
| 4 | Why 911 Is the Emergency Number | long | 85 |
| 5 | What If a 1-km Asteroid Hit New York? | long | **90** |
| 6 | Why AMBULANCE Is Written Backwards | short | **92** |
| 7 | What If the Cascadia Fault Ruptured Tomorrow? | long | **90** |
| 8 | Why Stop Signs Are Octagons | short | 83 |

Only one wording per topic was scored in the first pass. `generate_titles` was then run on the two lowest scorers:

**#2 Yellowstone (long), original 82:**
| Title | Score |
|---|---|
| Surviving a Yellowstone Eruption: Is It Possible? | 93 |
| Could Yellowstone Destroy Civilization? | 91 |
| The Truth About a Yellowstone Super-Eruption | 89 |
| If Yellowstone Erupted Tomorrow, This Is What Happens | 89 |
| Yellowstone Erupts: The End of America? | 88 |

Recommendation: "If Yellowstone Erupted Tomorrow, This Is What Happens" keeps the "what if" search phrase (89). "Destroy Civilization" and "End of America" overstate what USGS says, so avoid them given this channel's fact-check standard.

**#8 Stop signs (Short), original 83:**
| Title | Score |
|---|---|
| The weird reason stop signs look like this | 94 |
| The hidden logic behind stop sign shapes | 91 |
| Why you never see a round stop sign | 90 |
| The real story behind the 8-sided stop sign | 90 |
| The secret reason stop signs are octagons | 88 |

(vidIQ added hashtags; strip them from the title and put them in the description.) Recommendation: "The real story behind the 8-sided stop sign" (90). It promises only what the sourced story delivers. "The weird reason" scores higher but over-promises.
Note: the topic list says "What if the Cascadia fault went?" The working title above is clearer. "Tomorrow" is slightly clickbaity; consider "What If" + a time-neutral phrasing and test.

---

## 4. Scripts and outlines

Narration is written for about 150 words per minute. `[VISUAL]` cues are suggestions. Bracketed numbers marked VERIFY must be filled from the verification steps above.

### SHORT 6: Why AMBULANCE is written backwards (about 35s)
1. HOOK (0-3s) [VISUAL: ambulance front, flipped text]: "Why does ambulance say AMBULANCE backwards?"
2. (3-10s) "You're not meant to read it. You're meant to read it in your mirror."
3. (10-22s) [VISUAL: driver's rearview mirror, text flips to normal] "A mirror flips everything left to right. So the word is flipped first, and the mirror flips it back. The driver ahead reads it instantly, without thinking."
4. (22-32s) "That second matters. A driver who has to puzzle out a word is a driver who brakes late."
5. CLOSE (32-35s): "Next time you see one, check your mirror." Caption note: the origin of the practice is unclear. **Do not claim an inventor.**

### SHORT 3: Why school buses are that exact yellow (about 50s)
1. HOOK: "Every school bus in America is the same yellow. That wasn't an accident, and it wasn't a coincidence."
2. "In April 1939 a professor named Frank Cyr gathered state officials and engineers at Teachers College, Columbia."
3. "He wanted one national standard for school buses, instead of 48 different ideas."
4. "On the wall: shades of yellow running to orange. The group picked one." [VISUAL: swatch strip]
5. "It was officially named National School Bus Chrome. The reason: you can see it from far away, and black letters stand out on it."
6. "Cyr himself said it looked more orange than yellow."
7. CLOSE: "The color has a formula on file. It's a standard, not a guess." (VERIFY: where the formula is kept; one source says the National Bureau of Standards.)
Do not include the "peripheral vision" claim until verified.

### SHORT 8: Why stop signs are octagons (about 40s)
1. HOOK: "Stop signs weren't always red. Or eight-sided."
2. "The first ones, around 1915, were square and plain."
3. "They were yellow, because red paint faded back then." [VISUAL: yellow sign]
4. "In 1922 a standards committee gave the sign its own shape: the octagon. No other sign uses it."
5. "The idea is simple: a unique shape tells you something before you can read it, at night, or in the glare."
6. CLOSE: "So the next time you stop, you're obeying a shape that was designed in 1922 to be unmistakable." (Final line is a safe summary; no "from behind" claim.)
Verify the 1915 "square" claim before use, or say "early stop signs".

### LONG 1: Why Americans refrigerate eggs and Brits don't (8-10 min)
- Cold open (0:00-0:30): both fridges. "One of these is wrong. Neither is."
- Chapter 1 (0:30-2:30): what an egg actually is. The shell is porous, and the cuticle (bloom) seals pores.
- Chapter 2 (2:30-4:30): the American way. USDA wash rules. Washing removes the cuticle, which means the egg needs cold.
- Chapter 3 (4:30-6:30): the British way. Unwashed eggs, hen vaccination (Lion Code). Show the shelf at a UK store.
- Chapter 4 (6:30-8:00): why the US never switched. The FDA 2004 position, cost, scale, inertia. Put "one explanation" language on the cold-chain theory.
- Chapter 5 (8:00-9:00): what to do on holiday. Eggs bought in the US stay cold, and once chilled they must stay cold (condensation). VERIFY with USDA.
- Close and comment bait: "Where do YOU keep your eggs?" Pin a comment asking for country and shelf.

### LONG 2: What if Yellowstone erupted? (10-12 min)
- Open: Old Faithful, then a sky going dark.
- Ch.1: what Yellowstone is. A caldera, not a cone. Three giant eruptions (2.1M, 1.3M, 640K years ago).
- Ch.2: the odds. USGS: exceedingly low. Alert level Normal. Say why scientists are not worried.
- Ch.3: hour 0. Wyoming, Montana, Idaho: pyroclastic flows and heavy ash within hundreds of km.
- Ch.4: days 1-7. The ash map from the USGS 2014 model. Roofs, power, flights, crops. Use "centimeters to more than a meter near the park, millimeters at NYC, LA and Miami".
- Ch.5: months-years. Climate effect and food impact (VERIFY wording with USGS or a published model).
- Ch.6: the likely reality: hydrothermal explosions. This is the realistic hazard.
- Close: "It will probably never happen on a human timescale. Here's how we'd know." Monitoring by USGS and the YVO.

### LONG 4: Why 911 (6-8 min)
- Cold open: before 911, you called the operator or a seven-digit number for the police.
- Ch.1: the problem. Dozens of numbers, no national standard.
- Ch.2: 1967. The President's Commission recommends one number. FCC and AT&T meet (Nov 1967). AT&T announces 911 on Jan 12, 1968.
- Ch.3: why 911 (VERIFY, then script): three digits, easy, unused as a code.
- Ch.4: the race. A small independent telephone company in Haleyville, Alabama, beats AT&T. First call Feb 16, 1968, a ceremonial call.
- Ch.5: spread across the US. Nome, Huntington. Reach: the gap years before it was everywhere.
- Close: what 911 became (text-to-911, location data). VERIFY a current stat.

### LONG 5: What if a 1-km asteroid hit New York? (10-12 min) **NUMBERS PENDING**
- Open: the sky, a bright star that does not move.
- Structure: a clock. T-minus (detection and warning), T=0 (entry), T+seconds (impact), T+minutes (blast), T+hours (tsunami or ejecta), T+days, T+years.
- Ch.1: size check. 1 km, a "global-ish" class rather than a dinosaur-killer. Frame honestly (VERIFY from NASA CNEOS).
- Ch.2: what the impact calculator says (crater, fireball, overpressure, seismic, by distance). **Fill from the run.**
- Ch.3: by borough or by distance ring. Manhattan, Brooklyn, New Jersey, Long Island, New England. Pair with the Sandia finding about wide-area damage.
- Ch.4: aftermath: dust, climate, the regional economy.
- Ch.5: **the reassuring turn**: NASA tracks near-Earth objects, DART (2022) showed we can deflect an asteroid. VERIFY DART details.
- Close: "No known asteroid this size is headed our way."

### LONG 7: What if Cascadia went? (10-12 min)
- Open: a quiet Seattle or Portland morning.
- Ch.1: the fault. The Juan de Fuca plate sliding under North America: a subduction zone about 700 miles long (NOAA), Cape Mendocino to northern Vancouver Island.
- Ch.2: the evidence. January 1700, ghost forests and Japan's tsunami records.
- Ch.3: the odds. USGS 2025: about 10-15% in 50 years for the full margin. Be exact. This is not a "overdue" claim.
- Ch.4: the shaking: several minutes (DOGAMI has said 3-5). Do not give an intensity number until sourced.
- Ch.5: the tsunami: roughly 10 to 30 minutes after shaking begins on the Oregon coast, depending on location (sources differ).
- Ch.6: western Oregon: bridges, fuel, water, power. Use only the supported themes (see fact-check 7); no casualty number until the plan itself is read.
- Ch.7: what's being done. Early warning (ShakeAlert), building codes, tsunami sirens.
- Close: practical: two-weeks kit. A useful, non-fearful ending.

---

## 5. Open items before production
1. **Asteroid:** impact figures computed from the paper's equations (see fact-check 5). Still open: web-calculator cross-check, ground zero and land-vs-ocean choice, a sourced aftermath section, and whether any known 1 km asteroid has a non-zero impact probability (not verified).
2. **911:** reasons are secondary-sourced only (hedge the wording). Haleyville setup time (under a week vs five weeks) still open; check NENA's history page.
3. **Stop sign:** settled. "From behind" dropped, committee wording softened to "1920s, highway officials".
4. **School bus:** settled. Peripheral-vision claim out, "no national standard before 1939" wording.
5. **Cascadia:** timings settled as ranges (see fact-check 7). Oregon Resilience Plan numbers are now primary-sourced (see fact-check 7). Still open: ODOT 2019 quote wording and ShakeAlert.
6. **Eggs:** vaccination dates (UK Lion Code start year) and the UK case-count figure still unchecked.
7. Brand the channel before any recording (this repo currently has no CLAUDE.md or brand notes).
