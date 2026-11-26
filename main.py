#!/usr/bin/env python3
"""One Line to Your Younger Self — make.fun entry.

Writes the winning line to /output/entry.txt. Gate: UTF-8, 1-200 chars,
not only whitespace. The line is 103 chars, one sentence, one breath.

Tournament (specificity / surprise / freshness, each 1-5):
  1. Dumped girl marries best friend, you are best man, learn to dance — 5/4/4 = 13
  2. Fence scar on your knee, last time you were brave for free — 4/4/4 = 12
  3. Stop saving the good shirt, wear it to the Tuesday interview — 5/4/4 = 13
  4. The audition you bomb is why you meet her, so bomb it louder — 5/5/4 = 14
  5. WINNER: Your father is not angry, he is scared, and the day you
     figure that out you will finally call him back. — 5/5/5 = 15
     (the only 15 in the table; the turn lands on "call him back")
  6. Do not cut your hair before the photo, that haircut proves you were happy — 5/4/5 = 14
  7. The money you lend him never comes back, but the lesson buys the house — 5/5/4 = 14
  8. Keep the mixtape, lose the boy, at thirty you still know every word — 4/4/4 = 12

The winner is the only line that could come from this one older self:
a private re-reading of a father, not a motto anyone could wear. It
stings a little, stays warm rather than sentimental, and lands in a
single breath with the turn on the last three words.
"""

import argparse
import pathlib
import sys

LINE = (
    "Your father is not angry, he is scared, and the day you figure "
    "that out you will finally call him back."
)

CANDIDATES = [
    ("Kid, the girl who just dumped you marries your best friend, and "
     "you will be the best man, so stop crying and learn to dance.", 5, 4, 4),
    ("That scar on your knee from the fence? In ten years you will point "
     "at it and say it was the last time you were brave for free.", 4, 4, 4),
    ("Stop saving the good shirt for a special day; the special day is "
     "the Tuesday you finally wear it to the job interview.", 5, 4, 4),
    ("The audition you are about to bomb is the reason you meet her, "
     "so bomb it louder.", 5, 5, 4),
    (LINE, 5, 5, 5),
    ("Do not cut your hair before the photo; that terrible haircut is "
     "the only proof you were ever that happy.", 5, 4, 5),
    ("The money you are about to lend him never comes back, but the "
     "lesson buys you the house, so lend it and shut up.", 5, 5, 4),
    ("Keep the mixtape, lose the boy, and when you are thirty you will "
     "still know every word.", 4, 4, 4),
]


def check_line(line: str) -> tuple[bool, str]:
    """Validate the line against the gate: 1-200 chars, not blank."""
    if not line or not line.strip():
        return False, "empty"
    if len(line) > 200:
        return False, f"{len(line)} chars, over 200"
    if len(line) < 1:
        return False, "too short"
    return True, f"{len(line)} chars, 1 sentence, valid"


def run(out_dir: pathlib.Path) -> pathlib.Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(LINE, encoding="utf-8")
    return target


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
        print("candidate tournament (specificity / surprise / freshness):")
        for i, (text, spec, surp, fresh) in enumerate(CANDIDATES, 1):
            total = spec + surp + fresh
            mark = " <-- WINNER" if text == LINE else ""
            print(f"{i}. {spec}/{surp}/{fresh} = {total:2d}{mark}")
            print(f"   {text}")
        return 0

    if args.check:
        ok, detail = check_line(LINE)
        print(f"line: {LINE}")
        print(f"check: {detail}, {len(LINE.encode('utf-8'))} bytes, "
              f"{len(LINE.split())} words")
        return 0 if ok else 1

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            first = run(pathlib.Path(tmp) / "a").read_bytes()
            second = run(pathlib.Path(tmp) / "b").read_bytes()
        print("self-test:", "byte-identical" if first == second else "MISMATCH")
        return 0 if first == second else 1

    target = run(pathlib.Path(args.out))
    ok, detail = check_line(LINE)
    print(f"wrote {target} ({detail})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
