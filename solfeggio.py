#! /usr/bin/python

import random
from midiutil.MidiFile import MIDIFile

MAJOR_RUNS = [
    [[0, 2.0]],
    [[2, 2.0], [0, 2.0]],
    [[4, 2.0], [2, 1.0], [0, 2.0]],
    [[5, 2.0], [4, 1.0], [2, 1.0], [0, 2.0]],
    [[12, 2.0]],
    [[11, 2.0], [12, 2.0]],
    [[9, 2.0], [11, 1.0], [12, 2.0]],
    [[7, 2.0], [9, 1.0], [11, 1.0], [12, 2.0]],
]

MAJOR_MAIN_RUNS = [
    [[0, 2.0]],
    [[4, 2.0], [2, 1.0], [0, 2.0]],
    [[7, 2.0], [9, 1.0], [11, 1.0], [12, 2.0]],
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

MAJOR_MAIN_CHORDS = [
    [0, [0, 4, 7]], [0, [4, 7, 12]], [0, [-5, 0, 4]],
    [5, [5, 9, 12]], [5, [-3, 0, 5]], [5, [0, 5, 9]],
    [7, [-5, -1, 2]], [7, [-1, 2, 7]], [7, [2, 7, 11]],
]

MINOR_RUNS = [
    [[0, 2.0]],
    [[2, 2.0], [0, 2.0]],
    [[3, 2.0], [2, 1.0], [0, 2.0]],
    [[5, 2.0], [3, 1.0], [2, 1.0], [0, 2.0]],
    [[12, 2.0]],
    [[11, 2.0], [12, 2.0]],
    [[9, 2.0], [11, 1.0], [12, 2.0]],
    [[7, 2.0], [9, 1.0], [11, 1.0], [12, 2.0]],
    [[8, 2.0], [7, 1.0], [12, 2.0]],
    [[10, 2.0], [12, 2.0]],
]

MINOR_MAIN_RUNS = [
    [[0, 2.0]],
    [[3, 2.0], [2, 1.0], [0, 2.0]],
    [[7, 2.0], [9, 1.0], [11, 1.0], [12, 2.0]],
    [[12, 2.0]],
]

MINOR_CIRCLES = [
    [[0, 2.0], [2, 1.0], [-1, 1.0], [0, 2.0]],
    [[3, 2.0], [5, 1.0], [2, 1.0], [3, 2.0]],
    [[7, 2.0], [8, 1.0], [5, 1.0], [7, 2.0]],

    [[0, 2.0], [-1, 1.0], [2, 1.0], [0, 2.0]],
    [[3, 2.0], [2, 1.0], [5, 1.0], [3, 2.0]],
    [[7, 2.0], [5, 1.0], [8, 1.0], [7, 2.0]],
]

MINOR_MAIN_CHORDS = [
    [0, [0, 3, 7]], [0, [3, 7, 12]], [0, [-5, 0, 3]],
    [5, [5, 8, 12]], [5, [-4, 0, 5]], [5, [0, 5, 8]],
    [7, [-5, -2, 2]], [7, [-1, 2, 7]], [7, [2, 7, 10]],
]

MAJOR = [ MAJOR_RUNS, MAJOR_MAIN_RUNS, MAJOR_CIRCLES, MAJOR_MAIN_CHORDS ]
MINOR = [ MINOR_RUNS, MINOR_MAIN_RUNS, MINOR_CIRCLES, MINOR_MAIN_CHORDS ]

KEYS = [
    [ "C-major", 48, MAJOR ],
    [ "G-major", 43, MAJOR ],
    [ "A-minor", 45, MINOR ],
]

VOLUME_TABLE = [ 0, 100, 90, 80, 70 ]

class Generator:
    def __init__(self, tempo = 120):
        self.midi_file = MIDIFile(1)
        self.midi_file.addTrackName(0, 0, "track")
        self.midi_file.addTempo(0, 0, tempo)

        self.current_time = 1

    def add_pause(self, length = 1):
        self.current_time = self.current_time + length

    def add_chord(self, base, notes, length = 1):
        for note in notes:
            self.midi_file.addNote(0, 0, base + note, self.current_time, length, VOLUME_TABLE[len(notes)])
        self.add_pause(length)

    def add_pattern(self, base, pattern):
        for item in pattern:
            length = item[len(item) - 1]
            self.add_chord(base, item[0 : len(item) - 1], length)

    def write(self, filename):
        output_file = open(filename, 'wb')
        self.midi_file.writeFile(output_file)
        output_file.close()

def AddPreparations(generator, base, tonality, repeats = 3):
    [patterns, main_patterns, circles, main_chords] = tonality

    generator.add_chord(base, main_chords[0][1], 4)
    generator.add_pause(2)

    for i in xrange(0, repeats):
        for note in main_chords[0][1]:
            generator.add_chord(base, [ note ], 2)

        generator.add_pause(2)

    generator.add_pause(4)

    for pattern in patterns:
        for i in xrange(0, repeats):
            generator.add_pattern(base, pattern)
            generator.add_pause(2)

    generator.add_pause(4)

    for circle in circles:
        for i in xrange(0, repeats):
            generator.add_pattern(base, circle)
            generator.add_pause(2)

    generator.add_pause(4)

    chord_root = 0
    for chord in main_chords:
        for i in xrange(0, repeats):
            generator.add_chord(base, chord[1], 2)
            generator.add_pause(1)

            for note in chord[1]:
                generator.add_chord(base, [ note ], 2)

            if chord_root == chord[0]:
                generator.add_pause(2)
            else:
                generator.add_pause(4)

    generator.add_pause(2)

    generator.add_pause(8)

def GenerateRandomRuns(base, tonality, patterns, filename, tasks = 500):
    generator = Generator()

    AddPreparations(generator, base, tonality)

    for i in range(0, tasks):
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

def GenerateRandomSequences(base, tonality, patterns, filename, length, pause = 1, tasks = 500):
    generator = Generator()

    AddPreparations(generator, base, tonality)

    for i in range(0, tasks):
        chosen_patterns = [random.choice(patterns) for i in range(0, length)]

        for pattern in chosen_patterns:
            generator.add_pattern(base, pattern[0:1])
            generator.add_pause(pause)

        generator.add_pause(2)

        for pattern in chosen_patterns:
            generator.add_pattern(base, pattern)
            generator.add_pause()

        generator.add_pause(4)

    generator.write(filename)

def GenerateSingRandomIntervals(base, tonality, patterns, filename, tasks = 200, repeats = 10):
    generator = Generator()

    AddPreparations(generator, base, tonality)

    for i in range(0, tasks):
        sampled_patterns = random.sample(patterns, 2)

        for pattern in sampled_patterns:
            generator.add_pattern(base, pattern)
            generator.add_pause(1)

        generator.add_pause(2)

        for j in range(0, repeats):
            for pattern in sampled_patterns:
                generator.add_pattern(base, pattern[0:1])

            generator.add_pause(1)

        generator.add_pause(4)

    generator.write(filename)

def GenerateFindRandomHarmonicIntervals(base, tonality, patterns, filename, tasks = 200, repeats = 3):
    generator = Generator(80)

    AddPreparations(generator, base, tonality)

    for i in range(0, tasks):
        sampled_patterns = random.sample(patterns, 2)

        notes = [pattern[0][0] for pattern in sampled_patterns]

        if notes[0] > notes[1]:
            notes.reverse()
            sampled_patterns.reverse()

        for j in range(0, repeats):
            generator.add_chord(base, notes, 4)

        generator.add_pause(2)

        for pattern in sampled_patterns:
            generator.add_pattern(base, pattern[0:1])
            generator.add_pause(1)

        generator.add_pause(2)

        for pattern in reversed(sampled_patterns):
            generator.add_pattern(base, pattern[0:1])
            generator.add_pause(1)

        generator.add_pause(2)

        for pattern in sampled_patterns:
            generator.add_pattern(base, pattern)
            generator.add_pause(1)

        generator.add_pause(2)

        for j in range(0, repeats):
            generator.add_chord(base, notes, 4)

        generator.add_pause(4)

    generator.write(filename)

def FindPattern(patterns, note):
    for pattern in patterns:
        if pattern[0][0] == note:
            return [0, pattern]

        if pattern[0][0] + 12 == note:
            return [12, pattern]

        if pattern[0][0] - 12 == note:
            return [-12, pattern]

    return None

def GenerateFindChordsBassAndRoot(base, tonality, chords, patterns, filename, tasks = 400, repeats = 3):
    generator = Generator(80)

    AddPreparations(generator, base, tonality)

    for i in range(0, tasks):
        chord = random.choice(chords)

        for j in range(0, repeats):
            generator.add_chord(base, chord[1], 2)
            generator.add_pause(1)

            if j == repeats - 1:
                [delta, pattern] = FindPattern(patterns, chord[0])
                generator.add_pattern(base + delta, pattern)
                generator.add_pause(1)

                [delta, pattern] = FindPattern(patterns, chord[1][0])
                generator.add_pattern(base + delta, pattern)
                generator.add_pause(1)
            else:
                generator.add_chord(base, [ chord[0] ], 2)
                generator.add_pause(1)

                generator.add_chord(base, [ chord[1][0] ], 2)
                generator.add_pause(1)

    generator.add_pause(4)

    generator.write(filename)

for key in KEYS:
    [name, base, tonality] = key
    [patterns, main_patterns, circles, main_chords] = tonality

    track = 1

    GenerateRandomRuns(base, tonality, patterns, name + ("_%02d_runs_random.mid" % track))
    track = track + 1
    GenerateRandomSequences(base, tonality, patterns, name + ("_%02d_sequences_random_2.mid" % track), 2)
    track = track + 1
    GenerateRandomSequences(base, tonality, patterns, name + ("_%02d_sequences_random_2_nopause.mid" % track), 2, 0)
    track = track + 1
    GenerateRandomSequences(base, tonality, patterns, name + ("_%02d_sequences_random_3.mid" % track), 3)
    track = track + 1
    GenerateRandomSequences(base, tonality, patterns, name + ("_%02d_sequences_random_3_nopause.mid" % track), 3, 0)
    track = track + 1
    GenerateRandomSequences(base, tonality, patterns, name + ("_%02d_sequences_random_5_nopause.mid" % track), 5, 0, 300)
    track = track + 1
    GenerateRandomSequences(base, tonality, patterns, name + ("_%02d_sequences_random_10_nopause.mid" % track), 10, 0, 200)
    track = track + 1

    GenerateSingRandomIntervals(base, tonality, main_patterns, name + ("_%02d_intervals_sing_simple_pt1.mid" % track))
    track = track + 1
    GenerateSingRandomIntervals(base, tonality, main_patterns, name + ("_%02d_intervals_sing_simple_pt2.mid" % track))
    track = track + 1

    GenerateSingRandomIntervals(base, tonality, patterns, name + ("_%02d_intervals_sing_hard_pt1.mid" % track))
    track = track + 1
    GenerateSingRandomIntervals(base, tonality, patterns, name + ("_%02d_intervals_sing_hard_pt2.mid" % track))
    track = track + 1

    GenerateFindRandomHarmonicIntervals(base, tonality, main_patterns, name + ("_%02d_harmonic_intervals_simple_find_pt1.mid" % track))
    track = track + 1
    GenerateFindRandomHarmonicIntervals(base, tonality, main_patterns, name + ("_%02d_harmonic_intervals_simple_find_pt2.mid" % track))
    track = track + 1

    GenerateFindRandomHarmonicIntervals(base, tonality, patterns, name + ("_%02d_harmonic_intervals_hard_find_pt1.mid" % track))
    track = track + 1
    GenerateFindRandomHarmonicIntervals(base, tonality, patterns, name + ("_%02d_harmonic_intervals_hard_find_pt2.mid" % track))
    track = track + 1

    GenerateFindChordsBassAndRoot(base, tonality, main_chords, patterns, name + ("_%02d_find_main_chords_bass_and_root_pt1.mid" % track))
    track = track + 1

    GenerateFindChordsBassAndRoot(base, tonality, main_chords, patterns, name + ("_%02d_find_main_chords_bass_and_root_pt2.mid" % track))
    track = track + 1
