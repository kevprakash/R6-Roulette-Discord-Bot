# R6Roulette
A discord bot for getting random team compositions and loadouts for Rainbow Six: Siege. Teams and loadouts should be more or less feasible to play with.

## Command
### /roulette
**Params**:
- *side*: Choose whether your team is starting the match on Attack or Defense
- *rounds_per_half*: How many rounds before teams swap sides (3 for (un)ranked, 6 for competitions)
- *player1* to *player5*: Discord @s of who you want to generate for
- *ban1* to *ban4*: Which (if any) operators are banned for this match
- *silly*: If false (which is default), fewer operators can be selected for the soft destruction role and only a select few operators can get primary shotguns

**Output**:

A multi-page embed with the following:
- One page per round
  - Loadout for each player for the round
    - Operator \[Optionally, role they are filling]
    - Primary weapon
    - Secondary weapon
    - Gadget
  - Generates *rounds_per_half* * 2 + 4 rounds
    - Last 4 rounds are for overtime
- Can switch through pages for 10 minutes after the last page swap, then it times out
