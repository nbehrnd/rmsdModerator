
# Table of Contents

1.  [rmsdModerators](#orgdc20687)
    1.  [Background](#org4bd5a1f)
    2.  [Prerequisites](#org635e156)
    3.  [Typical session](#orgfaea38c)


<a id="orgdc20687"></a>

# rmsdModerators


<a id="org4bd5a1f"></a>

## Background

Complementary to a manual call of of Jimmy Charnley's
`calculate_rmsd.py` (<https://github.com/charnley/rmsd>) with two
model data A and B providing access to Kabsch and quaternion test, I
faced the situation to compare multiple structures (more than 50 per
run) where each model contains about a dozen of identical molecules.

An acceleration of the analysis was needed, since the the typical
batch wise comparison of such a round Robin tournament with \(n\)
model data has to consider \(n (n-1)/2\) tests to perform.  Specific
to Python, the "classical" approach is hampered since the GIL will
allow only a linear, sequential testing.

Script `multipro.py` is a moderator script to address the problem
differently, relaying the computation to multiple instances of
`calculate_rmsd.py` working independently from each other in
multiple cores of a CPU.  Meant as proof of concept only, the
script intentionally omits possible extensions (like an os.walk).


<a id="org635e156"></a>

## Prerequisites

While `calculate_rmsd.py` (version 1.3.2) is agnostic to either
Python2 or Python3, this script was written for Python3 only.
Place the moderator script, `multipro.py`, as well as the two \*.py
by Jimmy Charnley (`calculate_rmsd.py` and `__init__.py`) into the
same directory containing the `*.xyz` to scrutinize.  Beside these
three files and the five test `*.xyz`, the project contains this
README as `*.org` and `*.md` as well as a LICENCE (eleven files in
total).

Check the computer to be used.  At present, the maximum number of
tests performed simultaneously is set to equal 3 (three, line #79)
which balances nicely gain in performance with resources still
available for other (light weight) interaction with a quadrocore
processor computer.  Feel free to increase / adapt this number at
your own risk.  Launch the moderator script from the terminal by

    python3 multipro.py

At any time the execution of the script may be aborted (Ctrl + C).


<a id="orgfaea38c"></a>

## Typical session

With the five test `*.xyz` data provided, aiming to determine the
RMSD, the output on the CLI is the following:

    user@computer:~/Desktop/test/$ python3 multipro.py 
    python3 calculate_rmsd.py 00_1-O.xyz 01_2-O.xyz --reorder --use-reflections
    python3 calculate_rmsd.py 00_1-O.xyz 02_3-O.xyz --reorder --use-reflections
    python3 calculate_rmsd.py 00_1-O.xyz 03_4-O.xyz --reorder --use-reflections
    4.4884719544340745
    python3 calculate_rmsd.py 00_1-O.xyz 04_5-O.xyz --reorder --use-reflections
    4.33091155461067
    python3 calculate_rmsd.py 01_2-O.xyz 02_3-O.xyz --reorder --use-reflections
    4.444536428221002
    python3 calculate_rmsd.py 01_2-O.xyz 03_4-O.xyz --reorder --use-reflections
    6.009884394622477
    python3 calculate_rmsd.py 01_2-O.xyz 04_5-O.xyz --reorder --use-reflections
    3.9324928926740563
    python3 calculate_rmsd.py 02_3-O.xyz 03_4-O.xyz --reorder --use-reflections
    3.8063118346513205
    python3 calculate_rmsd.py 02_3-O.xyz 04_5-O.xyz --reorder --use-reflections
    2.7791567741970487
    python3 calculate_rmsd.py 03_4-O.xyz 04_5-O.xyz --reorder --use-reflections
    5.208090413262542
    5.657525349751654
    5.4498954394137105

