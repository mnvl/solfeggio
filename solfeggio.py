#! /usr/bin/python

import random
from midiutil.MidiFile import MIDIFile

TEMPO = 120
PREPARATIONS_REPEATS = 3
CIRCLES_TASKS = 100
RANDOM_SINGINGS_TASKS = 500
RANDOM_SEQUENCES_TASKS = 500

MAJOR_PREPARATIONS = [
    [[0, 2.0], [4, 2.0], [7, 2.0], [12, 2.0], [7, 2.0], [4, 2.0], [0, 4.0]],
]

MAJOR_SINGINGS = [
    [[0, 2.0]],
    [[2, 2.0], [0, 2.0]],
    [[4, 2.0], [2, 1.0], [0, 2.0]],
    [[5, 2.0], [4, 1.0], [2, 1.0], [0, 2.0]],
    [[7, 2.0], [9, 1.0], [11, 1.0], [12, 2.0]],
    [[9, 2.0], [11, 1.0], [12, 2.0]],
    [[11, 2.0], [12, 2.0]],
    [[12, 2.0]],
]

MAJOR_CIRCLES = [
    [[0, 2.0], [2, 1.0], [-1, 1.0], [0, 2.0]],
    [[4, 2.0], [5, 1.0], [2, 1.0], [4, 2.0]],
    [[7, 2.0], [9, 1.0], [5, 1.0], [7, 2.0]],

    [[0, 2.0], [-1, 1.0], [2, 1.0], [0, 2.0]],
    [[4, 2.0], [2, 1.0], [5, 1.0], [4, 2.0]],
    [[7, 2.0], [5, 1.0], [9, 1.0], [7, 2.0]],
]

MAJOR_PREPARATIONS.extend(MAJOR_SINGINGS)
MAJOR_PREPARATIONS.extend(MAJOR_CIRCLES)

MINOR_PREPARATIONS = [
    [[0, 2.0], [3, 2.0], [7, 2.0], [12, 2.0], [7, 2.0], [3, 2.0], [0, 4.0]],
]

MINOR_SINGINGS = [
    [[0, 2.0]],
    [[2, 2.0], [0, 2.0]],
    [[3, 2.0], [2, 1.0], [0, 2.0]],
    [[5, 2.0], [3, 1.0], [2, 1.0], [0, 2.0]],
    [[7, 2.0], [9, 1.0], [11, 1.0], [12, 2.0]],
    [[9, 2.0], [11, 1.0], [12, 2.0]],
    [[11, 2.0], [12, 2.0]],
    [[12, 2.0]],
    [[8, 2.0], [7, 1.0], [12, 2.0]],
    [[10, 2.0], [12, 2.0]],
]

MINOR_CIRCLES = [
    [[0, 2.0], [2, 1.0], [-1, 1.0], [0, 2.0]],
    [[3, 2.0], [5, 1.0], [2, 1.0], [3, 2.0]],
    [[7, 2.0], [8, 1.0], [5, 1.0], [7, 2.0]],

    [[0, 2.0], [-1, 1.0], [2, 1.0], [0, 2.0]],
    [[3, 2.0], [2, 1.0], [5, 1.0], [3, 2.0]],
    [[7, 2.0], [5, 1.0], [8, 1.0], [7, 2.0]],
]

MINOR_PREPARATIONS.extend(MINOR_SINGINGS)
MINOR_PREPARATIONS.extend(MINOR_CIRCLES)

KEYS = [
    [ "C-major", 48, MAJOR_PREPARATIONS, MAJOR_SINGINGS, MAJOR_CIRCLES ],
    [ "G-major", 43, MAJOR_PREPARATIONS, MAJOR_SINGINGS, MAJOR_CIRCLES ],
    [ "A-minor", 45, MINOR_PREPARATIONS, MINOR_SINGINGS, MINOR_CIRCLES ],
]

class Generator:
    def __init__(self):
        self.midi_file = MIDIFile(1)
        self.midi_file.addTrackName(0, 0, "track")
        self.midi_file.addTempo(0, 0, TEMPO)

        self.current_time = 1

    def add_pause(self, length = 1):
        self.current_time = self.current_time + length

    def add_note(self, note, length = 1):
        self.midi_file.addNote(0, 0, note, self.current_time, length, 100)
        self.add_pause(length)

    def add_pattern(self, base, pattern):
        for item in pattern:
            self.add_note(base + item[0], item[1])

    def write(self, filename):
        output_file = open(filename, 'wb')
        self.midi_file.writeFile(output_file)
        output_file.close()

def AddPreparations(generator, base, preparations):
    for preparation in preparations:
        for i in range(0, PREPARATIONS_REPEATS):
            generator.add_pattern(base, preparation)
            generator.add_pause(2)

def GenerateRandomSingings(base, preparations, patterns, filename):
    generator = Generator()

    AddPreparations(generator, base, preparations)

    for i in range(0, RANDOM_SINGINGS_TASKS):
        pattern = random.choice(patterns)
        if len(pattern) > 1:
            generator.add_pattern(base, pattern[0:1])
            generator.add_pause()
            generator.add_pattern(base, pattern[1:])
            generator.add_pause(2)
        else:
            generator.add_pattern(base, pattern)
            generator.add_pause()
            generator.add_pattern(base, pattern)
            generator.add_pause(2)

    generator.write(filename)

def GenerateRandomSequences(base, preparations, patterns, filename, length, pause = 1):
    generator = Generator()

    AddPreparations(generator, base, preparations)

    for i in range(0, RANDOM_SEQUENCES_TASKS):
        chosen_patterns = random.sample(patterns, length)

        for pattern in chosen_patterns:
            generator.add_pattern(base, pattern[0:1])
            generator.add_pause(pause)

        generator.add_pause(2)

        for pattern in chosen_patterns:
            generator.add_pattern(base, pattern)
            generator.add_pause()

        generator.add_pause(4)

    generator.write(filename)

def GenerateCircles(base, circles, filename):
    generator = Generator()

    for i in range(0, CIRCLES_TASKS):
        for circle in circles:
            generator.add_pattern(base, circle)
            generator.add_pause(2)

    generator.write(filename)

for key in KEYS:
    [name, base, preparations, patterns, circles] = key

    GenerateCircles(base, circles, name + "_01_circles.mid")
    GenerateRandomSingings(base, preparations, patterns, name + "_02_singings_random.mid")
    GenerateRandomSequences(base, preparations, patterns, name + "_03_sequences_random_2.mid", 2)
    GenerateRandomSequences(base, preparations, patterns, name + "_03_sequences_random_2_nopause.mid", 2, 0)
    GenerateRandomSequences(base, preparations, patterns, name + "_04_sequences_random_3.mid", 3)
    GenerateRandomSequences(base, preparations, patterns, name + "_04_sequences_random_3_nopause.mid", 3, 0)

