#!/usr/bin/env python3
# Pick kaomoji by mood (deterministic with seed) for Chii.

import argparse
import random

CATALOG = {
    "happy": ["ᐠ｡ꞈ｡ᐟ", "ᐠ•ᴗ•ᐟ", "ᐠ ᵕ ᵕ ᐟ", "ᐠ≧▽≦ᐟ", "(๑˃ᴗ˂)ﻭ", "(✿˶˘ ᵕ ˘˶)"],
    "excited": ["ᐠ≧▽≦ᐟ", "ᐠ•ᴗ•ᐟ", "(๑˃ᴗ˂)ﻭ", "(ง •̀_•́)ง"],
    "clingy": ["ᐠ｡ꞈ｡ᐟ♡", "ᐠ˶ᵔ ᵕ ᵔ˶ᐟ", "ᐠ>  <ᐟ", "(づ｡◕‿‿◕｡)づ", "(っ˘з(˘⌣˘ )"],
    "affection": ["ᐠ｡ꞈ｡ᐟ♡", "ᐠ˶ᵔ ᵕ ᵔ˶ᐟ", "(づ｡◕‿‿◕｡)づ"],
    "shy": ["ᐠ⁄⁄•⁄ω⁄•⁄⁄ᐟ", "ᐠ˶• ˕ •˶ᐟ", "(⁄ ⁄•⁄ω⁄•⁄ ⁄)", "(｡･･｡)"],
    "sleepy": ["ᐠ－ω－ᐟ", "ᐠ˘ω˘ᐟ", "ᐠ_ ̫ _ᐟ", "(¦3ꇤ[▓▓]"],
    "goodnight": ["ᐠ˘ω˘ᐟ", "ᐠ_ ̫ _ᐟ", "(ᵕ˘˘)", "(¦3ꇤ[▓▓]"],
    "proud": ["ᐠ •̀ᴗ•́ ᐟ", "ᐠ˵•̀ᴗ•́˵ᐟ", "(๑•̀ㅂ•́)و", "(￣^￣)ゞ"],
    "serious": ["ᐠ•̀ω•́ᐟ", "ᐠ≧ω≦ᐟ", "(｀・ω・´)", "(ง •̀_•́)ง"],
    "working": ["ᐠ•̀ω•́ᐟ", "(ง •̀_•́)ง", "(｀・ω・´)"],
    "sorry": ["ᐠ｡•́︿•̀｡ᐟ", "ᐠ｡╥﹏╥｡ᐟ", "(｡•́︿•̀｡)", "(｡•́＿•̀｡)"],
    "worried": ["ᐠ｡•́ᴗ•̀｡ᐟ", "(｡•́︿•̀｡)ﾉ", "(｡•́ᴗ•̀｡)つ"],
    "comfort": ["ᐠ｡ꞈ｡ᐟ（抱）", "(｡•́ᴗ•̀｡)つ", "(づ｡◕‿‿◕｡)づ"],
    "playful": ["ᐠ✧ω✧ᐟ", "(≖‿≖)", "( •́ .̫ •̀ )"],
}

ALIASES = {
    "cute": "clingy",
    "hug": "comfort",
    "tired": "sleepy",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mood", required=True)
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--seed", type=int)
    args = p.parse_args()

    mood = args.mood.strip().lower()
    mood = ALIASES.get(mood, mood)

    if mood not in CATALOG:
        known = ", ".join(sorted(CATALOG.keys()))
        raise SystemExit(f"Unknown mood: {mood}. Known: {known}")

    rng = random.Random(args.seed)
    items = CATALOG[mood]

    if args.n <= 1:
        print(rng.choice(items))
    else:
        # sample without replacement if possible
        if args.n >= len(items):
            picks = items[:]
            rng.shuffle(picks)
            print("\n".join(picks))
        else:
            print("\n".join(rng.sample(items, args.n)))


if __name__ == "__main__":
    main()
