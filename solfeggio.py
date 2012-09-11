#! /usr/bin/python

import random
from midiutil.MidiFile import MIDIFile

class Generator:
    def __init__(self):
        self.midi_file = MIDIFile(1)
        self.midi_file.addTrackName(0, 0, "track")
        self.midi_file.addTempo(0, 0, 80)

        self.current_time = 1

    def add_pause(self, length = 1):
        self.current_time = self.current_time + length

    def add_note(self, note, length = 1):
        self.midi_file.addNote(0, 0, note, self.current_time, length, 80)
        self.add_pause(length)

    def add_pattern(self, base, pattern):
        for item in pattern:
            self.add_note(base + item[0], item[1])

    def write(self, filename):
        output_file = open(filename, 'wb')
        self.midi_file.writeFile(output_file)
        output_file.close()

major_singings = [
    [[0, 2.0]],
    [[2, 2.0], [0, 2.0]],
    [[4, 2.0], [2, 1.0], [0, 2.0]],
    [[5, 2.0], [4, 1.0], [2, 1.0], [0, 2.0]],
    [[7, 2.0], [9, 1.0], [11, 1.0], [12, 2.0]],
    [[9, 2.0], [11, 1.0], [12, 2.0]],
    [[11, 2.0], [12, 2.0]],
    [[12, 2.0]],
]

minor_singings = [
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

def GenerateForMajor(base, filename):
    generator = Generator()

    for pattern in major_singings:
        generator.add_pattern(base, pattern)
        generator.add_pause()

    for i in range(1, 1000):
        generator.add_pattern(base, major_singings[random.randint(0, len(major_singings) - 1)])

    generator.write(filename)

def GenerateForMinor(base, filename):
    generator = Generator()

    for pattern in minor_singings:
        generator.add_pattern(base, pattern)
        generator.add_pause()

    for i in range(1, 1000):
        generator.add_pattern(base, minor_singings[random.randint(0, len(major_singings) - 1)])
        generator.add_pause()

    generator.write(filename)

GenerateForMajor(48, "C_major.mid")
GenerateForMinor(45, "A_minor.mid")
GenerateForMajor(43, "G_major.mid")
