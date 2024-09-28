import pandas as pd
import numpy as np
from random import randint, shuffle

operatorData = pd.read_csv("Data/Siege Operators.csv")
loadoutData = pd.read_csv("Data/Siege Loadouts.csv")

opNames = operatorData["Operator"].tolist()

roleDictDef = {
    "HBreach": "Hard Breach",
    "Denial": "Denial",
    "SBreach": "Destruction"
}

roleDictAtk = {
    "HBreach": "Hard Breach",
    "Denial": "Anti-denial",
    "SBreach": "Soft Destruction"
}


def getLoadout(attacker, requiredTag=None, takenOps=(), seriousMode=False):
    filteredData = operatorData[operatorData["Attacker"] == attacker]
    filteredData = filteredData[~filteredData["Operator"].isin(takenOps)]
    if requiredTag is not None:
        filteredData = filteredData[filteredData[requiredTag]]

    if seriousMode and (requiredTag == "SBreach"):
        mergedData = filteredData.merge(loadoutData, how='left', on="Operator")
        filteredData = mergedData[mergedData["Operator"].isin(["Smoke", "Mute", "Warden", "Kaid", "Goyo", "Alibi", "Maestro"])
                                    | mergedData["S1 Shotgun"] | mergedData["Gadget SD"]
                                    ]

    row = np.random.choice(filteredData.index.values, 1)[0]
    opData = filteredData.loc[row]

    op = opData["Operator"]
    roleDict = roleDictAtk if attacker else roleDictDef
    role = roleDict[requiredTag] if requiredTag is not None else ""
    primary = randint(1, opData["Primaries"])
    secondary = randint(1, opData["Secondaries"])
    gadget = randint(1, opData["Gadgets"])

    primary, secondary, gadget = fixAndTranslateLoadout(op, primary, secondary, gadget, requiredTag, opData, seriousMode=seriousMode)

    return op, role, primary, secondary, gadget


def fixAndTranslateLoadout(op, primary, secondary, gadget, requiredTag, opData, seriousMode=False):
    # print(op)
    operatorLoadout = loadoutData[loadoutData["Operator"] == op]
    p = s = g = None
    pShotgun = (primary == 1) and (operatorLoadout["P1 Shotgun"].all())
    sShotgun = (secondary == 1) and (operatorLoadout["S1 Shotgun"].all())

    if requiredTag == "HBreach":
        if operatorLoadout["G1"].iloc[0] == "Hard Breach":
            g = "Hard Breach"
    elif requiredTag == "Denial":
        if operatorLoadout["G2"].iloc[0] == "EMP":
            g = "EMP"
    elif requiredTag == "SBreach":
        if operatorLoadout["Gadget SD"].iloc[0]:
            pass
        elif operatorLoadout["S1 Shotgun"].all():
            s = operatorLoadout["S1"].iloc[0]
            sShotgun = True
        elif operatorLoadout["G3"].isin(["Breach Pad", "Impact"]).all():
            g = operatorLoadout["G3"].iloc[0]
        elif operatorLoadout["P1 Shotgun"].all():
            p = operatorLoadout["P1"].iloc[0]
            pShotgun = True

    seriousShotgun = op in ["Smoke", "Mute", "Warden", "Kaid", "Goyo", "Alibi", "Maestro", "Kali", "Deimos", "Amaru"]
    if (pShotgun and sShotgun) or (seriousMode and pShotgun and (not seriousShotgun)):
        primary = randint(2, opData["Primaries"]) if opData["Primaries"] > 2 else 2

    if seriousMode and (pShotgun and seriousShotgun):
        secondary = 1

    if p is None:
        p = str(operatorLoadout[["P1", "P2", "P3"]].iloc[0, primary - 1])
    if s is None:
        s = str(operatorLoadout[["S1", "S2", "S3"]].iloc[0, secondary - 1])
    if g is None:
        gadgetLoadout = set(operatorLoadout[["G1", "G2", "G3", "G4", "G5", "G6", "G7"]].values.flatten().tolist())
        gadgetLoadout = [x for x in gadgetLoadout if x == x]
        g = gadgetLoadout[gadget - 1]

    return p, s, g


def getTeam(attacker, players, bans, seriousMode=False):
    attackerReq = ["HBreach", "Denial", "SBreach"]
    defenderReq = ["Denial", "SBreach"]

    reqs = attackerReq if attacker else defenderReq
    reqIndex = 0
    n = len(players)
    loadouts = []
    takenOps = bans.copy()
    for i in range(n):
        req = reqs[reqIndex] if reqIndex < len(reqs) else None
        loadout = getLoadout(attacker, req, takenOps, seriousMode=seriousMode)
        loadouts.append(loadout)
        takenOps.append(loadout[0])
        reqIndex += 1

    shuffle(loadouts)

    return loadouts