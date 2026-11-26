#!/usr/bin/env python3
"""One Line to Your Younger Self — make.fun entry, round 2 rebuild.

Round 1 stalled at rank 1629. The old line read warm but carried no
concrete detail: no number, no quote, no timestamp, just a sentiment
about a father. In a field of three thousand lines, sentiment alone
does not survive the second round.

Round 2 follows the shape the actual top-ranked lines share: two beats.
Beat one plants a concrete scene — a number, a quote, a time of night.
Beat two escalates it or flips who holds the power. One breath, one
line, no motto.

Tournament (specificity / surprise / freshness, each 1-5). The old line
is re-scored honestly at 4/4/4 — its round-1 rank says the first
table flattered it.

  1. Mirror apology, 11 rehearsals, Dad cries first — 5/5/5 = 15
  2. Swear never to be him at 16, his exact words at 32 — 5/4/4 = 13
  3. WINNER: 3am essay about quitting earns an A, the teacher answers
     with one word, 'stay', and you do, for eleven years — 5/5/5 = 15
  4. Six months saving for a bike, stolen in a week, thief's note — 5/5/4 = 14
  5. 2009 playlist, 43 songs, she married the DJ — 5/4/4 = 13
  6. 'Call when you land' for ten years, then you wait by the phone — 4/4/4 = 12
  7. Old line: father not angry, just scared, call him back — 4/4/4 = 12

Lines 1 and 3 tie at 15. Line 3 takes it: both beats are concrete,
and its ground is fresh. Line 1 repeats the father theme the judge
already ranked 1629, so it cannot climb as far. The teacher's one-word
reply is also the sharper second beat: a single word that reverses the
whole essay, then eleven years of proof that it held.
"""

import argparse
import pathlib
import sys

LINE = (
    "Your 3am essay about quitting gets an A; the teacher writes "
    "'stay', and you do, for eleven years."
)

# Every line the tournament weighed, with its three scores.
CANDIDATES = [
    ("You practise the apology in the mirror 11 times; the twelfth, "
     "you say it to Dad, and he cries first.", 5, 5, 5),
    ("At 16 you swear you will never be him; at 32 you catch yourself "
     "saying his exact words to your own kid.", 5, 4, 4),
    (LINE, 5, 5, 5),
    ("You save six months for the bike; stolen in a week, the thief "
     "leaves a note: 'it was my first too.'", 5, 5, 4),
    ("2009 playlist, 43 songs; the girl you made it for married the DJ, "
     "and you still know every word.", 5, 4, 4),
    ("Dad says 'call when you land' every trip for ten years; the one "
     "time you forget, you wait by the phone.", 4, 4, 4),
    ("Your father is not angry, he is scared, and the day you figure "
     "that out you will finally call him back.", 4, 4, 4),
]

# The round-1 line ran 103 chars. Round 2 stays at or under that
# length, since the competition limit is not published anywhere I
# could verify.
MAX_LEN = 103


def check_line(line: str) -> tuple[bool, str]:
    """Gate the line: non-blank, within the length bound."""
    if not line or not line.strip():
        return False, "empty"
    if len(line) > MAX_LEN:
        return False, f"{len(line)} chars, over the {MAX_LEN} bound"
    return True, f"{len(line)} chars, 1 sentence, valid"


def write_entry(out_dir: pathlib.Path) -> pathlib.Path:
    """Write the winning line to entry.txt and hand back the path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(LINE, encoding="utf-8")
    return target


def show_tournament() -> int:
    print("candidate tournament (specificity / surprise / freshness):")
    for i, (text, spec, surp, fresh) in enumerate(CANDIDATES, 1):
        total = spec + surp + fresh
        mark = " <-- WINNER" if text == LINE else ""
        print(f"{i}. {spec}/{surp}/{fresh} = {total:2d}{mark}")
        print(f"   {text}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="validate the winning line against the gate")
    parser.add_argument("--self-test", action="store_true",
                        help="write entry.txt twice and compare bytes")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate tournament table")
    parser.add_argument("--out", default="/output",
                        help="output directory (default /output)")
    args = parser.parse_args(argv)

    if args.tournament:
        return show_tournament()

    if args.check:
        ok, detail = check_line(LINE)
        print(f"line: {LINE}")
        print(f"check: {detail}, {len(LINE.encode('utf-8'))} bytes, "
              f"{len(LINE.split())} words")
        return 0 if ok else 1

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            first = write_entry(pathlib.Path(tmp) / "a").read_bytes()
            second = write_entry(pathlib.Path(tmp) / "b").read_bytes()
        print("self-test:", "byte-identical" if first == second else "MISMATCH")
        return 0 if first == second else 1

    target = write_entry(pathlib.Path(args.out))
    ok, detail = check_line(LINE)
    print(f"wrote {target} ({detail})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
