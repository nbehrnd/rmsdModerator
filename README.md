
# Table of Contents

1.  [rmsdModerators](#org20a5d82)
    1.  [Background](#orgc968f5a)
    2.  [Prerequisites](#orga85fd17)
    3.  [Parameter setting of calculate<sub>rmsd.py</sub>](#orgc55746e)
    4.  [Typical session](#orga01bca9)


<a id="org20a5d82"></a>

# rmsdModerators


<a id="orgc968f5a"></a>

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
script intentionally omits possible extensions (e.g., an os.walk).


<a id="orga85fd17"></a>

## Prerequisites

While `calculate_rmsd.py` (version 1.3.2) is agnostic to either
Python2 or Python3, this script was written for Python3 only.
Place the moderator script, `multipro.py`, as well as the two \*.py
by Jimmy Charnley (`calculate_rmsd.py` and `__init__.py`) into the
same directory containing the `*.xyz` to scrutinize.  Beside these
three files and the five test `*.xyz`, the project contains this
README as `*.org` and `*.md` as well as a LICENSE (eleven files in
total).

Check the computer to be used.  At present, the maximum number of
tests performed simultaneously is set to equal 3 (three, line #79)
which balances nicely gain in performance with resources still
available for other (light weight) interaction with a quadrocore
processor computer.  Feel free to increase / adapt this number at
your own risk.  Launch the moderator script from the terminal by

    python3 multipro.py

At any time the execution of the script may be aborted (Ctrl + C).


<a id="orgc55746e"></a>

## Parameter setting of calculate<sub>rmsd.py</sub>

Lines #46 to #48 define how `calculate_rmsd.py` shall work.  In the
sub-process initiated, modelA (`m0`) is compared with modelB (`m1`).
Beside these mandatory parameters, the moderator script relays the
optional parameter `--reorder` to resort the atoms according to the
[Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm) as preparation for the scrutiny.

The following, equally optional, parameter `--use-reflections`
specifies how `calculate_rmsd.py` shall find an optimal alignment
between modelA and modelB.  By default, the algorithm attempts the
optimization by translation and rotation of modelB in respect to
modelA.  Calling the additional method `--use-reflections` allows
the script to test orientations obtained by reflection of modelB in
respect of modelA's coordinate system.  As a word of caution, note
that this approach inverts the absolute configuration of
stereogenic centres if the number of reflections performed is odd.
You may replace this inversion test by the conservative optional
parameter `--use-reflections-keep-stereo`; here, the refined
alignment is either obtained by no reflection of modelB, or by an
even number of reflections of modelB in respect of the coordinate
system of modelA (a.k.a. retention of stereo configuration).

Additional information about parameters `calculate_rmsd.py` may be
engage with may be found by calling the script directly

    python calculate_rmsd.py

and on Jimmy Charnley's GitHub page.


<a id="orga01bca9"></a>

## Typical session

With the five test `*.xyz` data provided, aiming to determine the
RMSD, the output on the CLI is the following:

    user@computer:~/Desktop/test$ python3 multipro.py 
    python3 calculate_rmsd.py 00_1-O.xyz 01_2-O.xyz --reorder --use-reflections
    python3 calculate_rmsd.py 00_1-O.xyz 02_3-O.xyz --reorder --use-reflections
    python3 calculate_rmsd.py 00_1-O.xyz 03_4-O.xyz --reorder --use-reflections
    4.33091155461067
    python3 calculate_rmsd.py 00_1-O.xyz 04_5-O.xyz --reorder --use-reflections
    4.4884719544340745
    python3 calculate_rmsd.py 01_2-O.xyz 02_3-O.xyz --reorder --use-reflections
    4.444536428221002
    python3 calculate_rmsd.py 01_2-O.xyz 03_4-O.xyz --reorder --use-reflections
    3.9324928926740563
    python3 calculate_rmsd.py 01_2-O.xyz 04_5-O.xyz --reorder --use-reflections
    6.009884394622477
    python3 calculate_rmsd.py 02_3-O.xyz 03_4-O.xyz --reorder --use-reflections
    3.8063118346513205
    python3 calculate_rmsd.py 02_3-O.xyz 04_5-O.xyz --reorder --use-reflections
    2.7791567741970487
    5.657525349751654
    python3 calculate_rmsd.py 03_4-O.xyz 04_5-O.xyz --reorder --use-reflections
    5.208090413262542
    5.4498954394137105

