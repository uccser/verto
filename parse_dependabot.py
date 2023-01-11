#!/usr/bin/env python3

import re
import sys

import subprocess

if len(sys.argv) <= 1:
    print("Please supply the ref as the first parameter")
    sys.exit(1)

proc = subprocess.run(
    f'git log {sys.argv[1]}..HEAD --author="dependabot" --grep="^Bump" --oneline --no-decorate',
    shell=True,
    stdout=subprocess.PIPE,
    text=True
)
lines = sorted(proc.stdout.splitlines())

warnings = []
output = []

p = re.compile(r"Bump ([a-zA-Z\/\-\_0-9]+) from ([0-9\.]+) to ([0-9\.]+)")
for (line, match) in map(lambda line:  (line, p.search(line)), lines):
    if not match:
        warnings.append(line)
        continue

    name, old, new = match.group(1, 2, 3)
    output.append(f"- Update {name} from {old} to {new}.")

print(*sorted(set(output)), sep="\n")

if warnings:
    print("Could not parse these lines")
    print(*warnings, sep="\n")
