#!/usr/bin/env python3
"""
Прост скрипт за генериране на MIDI файл от нотите на джаз парчето.
Използва стандартната библиотека без външни зависимости.
"""

import struct
import os

# MIDI constants
HEADER_CHUNK_TYPE = b'MThd'
TRACK_CHUNK_TYPE = b'MTrk'
HEADER_CHUNK_LENGTH = struct.pack('>I', 6)
TRACK_CHUNK_LENGTH_PLACEHOLDER = struct.pack('>I', 0)
FORMAT_1 = struct.pack('>h', 1)  # Multiple tracks
NUM_TRACKS = struct.pack('>h', 6)  # 6 tracks: trumpet, sax, piano, bass, drums, end
DIVISION = struct.pack('>h', 480)  # Ticks per quarter note

# MIDI events
NOTE_OFF = 0x80
NOTE_ON = 0x90
PROGRAM_CHANGE = 0xC0
CONTROL_CHANGE = 0xB0
META_EVENT = 0xFF
END_OF_TRACK = 0x2F
SET_TEMPO = 0x51

# Instruments (General MIDI program numbers)
TRUMPET = 56
TENOR_SAX = 57
ACOUSTIC_GRAND_PIANO = 0
ACOUSTIC_BASS = 32
DRUMS = 118  # Percussion

# Note mappings (MIDI note numbers)
# C4 = 60, D4 = 62, E4 = 64, F4 = 65, G4 = 67, A4 = 69, B4 = 71
# C5 = 72, D5 = 74, E5 = 76, F5 = 77, G5 = 79, A5 = 81, B5 = 83

NOTES = {
    'C,': 36, 'D,': 38, 'E,': 40, 'F,': 41, 'G,': 43, 'A,': 45, 'B,': 47,
    'C': 48, 'D': 50, 'E': 52, 'F': 53, 'G': 55, 'A': 57, 'B': 59,
    "c": 60, "d": 62, "e": 64, "f": 65, "g": 67, "a": 69, "b": 71,
    "c'": 72, "d'": 74, "e'": 76, "f'": 77, "g'": 79, "a'": 81, "b'": 83,
}

# Tempo: 180 BPM = 500000 microseconds per quarter note
TEMPO = 500000

# Ticks per beat
TPB = 480

# Time signatures and other meta events
TIME_SIGNATURE = bytes([0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08])
KEY_SIGNATURE = bytes([0xFF, 0x59, 0x02, 0x00, 0x00])  # C major


def write_var_length(value, data):
    """Write a variable-length quantity to the data list."""
    value &= 0x7F
    while value >= 0x80:
        data.append(0x80 | (value & 0x7F))
        value >>= 7
    data.append(value)


def write_midi_event(track_data, delta_time, status, data_bytes):
    """Write a MIDI event to the track data."""
    write_var_length(delta_time, track_data)
    track_data.append(status)
    track_data.extend(data_bytes)


def write_meta_event(track_data, delta_time, meta_type, meta_data):
    """Write a meta event to the track data."""
    write_var_length(delta_time, track_data)
    track_data.append(META_EVENT)
    track_data.append(meta_type)
    write_var_length(len(meta_data), track_data)
    track_data.extend(meta_data)


def create_trumpet_track():
    """Create trumpet track with main melody."""
    track_data = bytearray()
    
    # Program change to trumpet (channel 0)
    write_midi_event(track_data, 0, PROGRAM_CHANGE | 0, [TRUMPET])
    
    # Intro (4 bars rest)
    write_midi_event(track_data, TPB * 4, CONTROL_CHANGE | 0, [0x40, 127])  # Sustain off
    
    # Main theme
    # Bar 5: c4 e g c
    write_midi_event(track_data, 0, NOTE_ON | 0, [NOTES['c'], 80])
    write_midi_event(track_data, TPB, NOTE_OFF | 0, [NOTES['c'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 0, [NOTES['e'], 80])
    write_midi_event(track_data, TPB, NOTE_OFF | 0, [NOTES['e'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 0, [NOTES['g'], 80])
    write_midi_event(track_data, TPB, NOTE_OFF | 0, [NOTES['g'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 0, [NOTES["c'"], 80])
    write_midi_event(track_data, TPB, NOTE_OFF | 0, [NOTES["c'"], 0])
    
    # Continue with more notes...
    # For simplicity, we'll create a basic pattern
    
    # Simple melody pattern
    melody = [
        ('c', TPB), ('e', TPB), ('g', TPB), ("c'", TPB),
        ('e', TPB), ('d', TPB), ('c', TPB), ('B', TPB),
        ('A', TPB * 2), ('F', TPB), ('A', TPB), ('d', TPB),
        ('c', TPB), ('B', TPB), ('A', TPB), ('G', TPB),
    ]
    
    for note, duration in melody:
        write_midi_event(track_data, 0, NOTE_ON | 0, [NOTES[note], 80])
        write_midi_event(track_data, duration, NOTE_OFF | 0, [NOTES[note], 0])
    
    # End of track
    write_meta_event(track_data, 0, END_OF_TRACK, [])
    
    return bytes(track_data)


def create_piano_track():
    """Create piano track with chords."""
    track_data = bytearray()
    
    # Program change to piano (channel 3)
    write_midi_event(track_data, 0, PROGRAM_CHANGE | 3, [ACOUSTIC_GRAND_PIANO])
    
    # Intro rest
    write_midi_event(track_data, TPB * 4, CONTROL_CHANGE | 3, [0x40, 127])
    
    # C7 chord (C, E, G, Bb)
    write_midi_event(track_data, 0, NOTE_ON | 3, [NOTES['C'], 70])
    write_midi_event(track_data, 0, NOTE_ON | 3, [NOTES['E'], 70])
    write_midi_event(track_data, 0, NOTE_ON | 3, [NOTES['G'], 70])
    write_midi_event(track_data, 0, NOTE_ON | 3, [NOTES['B'], 65])  # Bb is B-1
    write_midi_event(track_data, TPB * 4, NOTE_OFF | 3, [NOTES['C'], 0])
    write_midi_event(track_data, 0, NOTE_OFF | 3, [NOTES['E'], 0])
    write_midi_event(track_data, 0, NOTE_OFF | 3, [NOTES['G'], 0])
    write_midi_event(track_data, 0, NOTE_OFF | 3, [NOTES['B'], 0])
    
    # F7 chord
    write_midi_event(track_data, 0, NOTE_ON | 3, [NOTES['F'], 70])
    write_midi_event(track_data, 0, NOTE_ON | 3, [NOTES['A'], 70])
    write_midi_event(track_data, 0, NOTE_ON | 3, [NOTES["c'"], 70])
    write_midi_event(track_data, 0, NOTE_ON | 3, [NOTES['e'], 65])  # Eb
    write_midi_event(track_data, TPB * 4, NOTE_OFF | 3, [NOTES['F'], 0])
    write_midi_event(track_data, 0, NOTE_OFF | 3, [NOTES['A'], 0])
    write_midi_event(track_data, 0, NOTE_OFF | 3, [NOTES["c'"], 0])
    write_midi_event(track_data, 0, NOTE_OFF | 3, [NOTES['e'], 0])
    
    # End of track
    write_meta_event(track_data, 0, END_OF_TRACK, [])
    
    return bytes(track_data)


def create_bass_track():
    """Create bass track."""
    track_data = bytearray()
    
    # Program change to bass (channel 4)
    write_midi_event(track_data, 0, PROGRAM_CHANGE | 4, [ACOUSTIC_BASS])
    
    # Intro rest
    write_midi_event(track_data, TPB * 4, CONTROL_CHANGE | 4, [0x40, 127])
    
    # Bass line: C, E, G, C
    write_midi_event(track_data, 0, NOTE_ON | 4, [NOTES['C,'], 75])
    write_midi_event(track_data, TPB, NOTE_OFF | 4, [NOTES['C,'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 4, [NOTES['E,'], 75])
    write_midi_event(track_data, TPB, NOTE_OFF | 4, [NOTES['E,'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 4, [NOTES['G,'], 75])
    write_midi_event(track_data, TPB, NOTE_OFF | 4, [NOTES['G,'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 4, [NOTES['C'], 75])
    write_midi_event(track_data, TPB, NOTE_OFF | 4, [NOTES['C'], 0])
    
    # F, A, C, F
    write_midi_event(track_data, 0, NOTE_ON | 4, [NOTES['F,'], 75])
    write_midi_event(track_data, TPB, NOTE_OFF | 4, [NOTES['F,'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 4, [NOTES['A,'], 75])
    write_midi_event(track_data, TPB, NOTE_OFF | 4, [NOTES['A,'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 4, [NOTES['C'], 75])
    write_midi_event(track_data, TPB, NOTE_OFF | 4, [NOTES['C'], 0])
    write_midi_event(track_data, 0, NOTE_ON | 4, [NOTES['F'], 75])
    write_midi_event(track_data, TPB, NOTE_OFF | 4, [NOTES['F'], 0])
    
    # End of track
    write_meta_event(track_data, 0, END_OF_TRACK, [])
    
    return bytes(track_data)


def create_drum_track():
    """Create drum track."""
    track_data = bytearray()
    
    # Program change to drums (channel 9)
    write_midi_event(track_data, 0, PROGRAM_CHANGE | 9, [DRUMS])
    
    # Drum pattern: Bass drum (36), Snare (38), Hi-hat (42)
    # Simple jazz pattern
    for _ in range(8):  # 8 bars
        # Bass drum on 1 and 3
        write_midi_event(track_data, 0, NOTE_ON | 9, [36, 80])
        write_midi_event(track_data, TPB//2, NOTE_OFF | 9, [36, 0])
        write_midi_event(track_data, 0, NOTE_ON | 9, [42, 60])
        write_midi_event(track_data, TPB//2, NOTE_OFF | 9, [42, 0])
        
        write_midi_event(track_data, TPB//2, NOTE_ON | 9, [42, 60])
        write_midi_event(track_data, TPB//2, NOTE_OFF | 9, [42, 0])
        
        # Snare on 2 and 4
        write_midi_event(track_data, 0, NOTE_ON | 9, [38, 70])
        write_midi_event(track_data, TPB//2, NOTE_OFF | 9, [38, 0])
        write_midi_event(track_data, 0, NOTE_ON | 9, [42, 60])
        write_midi_event(track_data, TPB//2, NOTE_OFF | 9, [42, 0])
        
        write_midi_event(track_data, TPB//2, NOTE_ON | 9, [42, 60])
        write_midi_event(track_data, TPB//2, NOTE_OFF | 9, [42, 0])
    
    # End of track
    write_meta_event(track_data, 0, END_OF_TRACK, [])
    
    return bytes(track_data)


def create_midi_file():
    """Create the complete MIDI file."""
    # Create header chunk
    header = HEADER_CHUNK_TYPE + HEADER_CHUNK_LENGTH + FORMAT_1 + NUM_TRACKS + DIVISION
    
    # Create tracks
    trumpet_track = create_trumpet_track()
    piano_track = create_piano_track()
    bass_track = create_bass_track()
    drum_track = create_drum_track()
    
    # Build track chunks
    tracks = []
    for track_data in [trumpet_track, piano_track, bass_track, drum_track]:
        track_chunk = TRACK_CHUNK_TYPE + struct.pack('>I', len(track_data)) + track_data
        tracks.append(track_chunk)
    
    # Combine all chunks
    midi_data = header + b''.join(tracks)
    
    return midi_data


def main():
    """Main function to generate MIDI file."""
    midi_data = create_midi_file()
    
    # Save to file
    output_path = '/home/user/13kpeev/60th_birthday_jazz.mid'
    with open(output_path, 'wb') as f:
        f.write(midi_data)
    
    print(f"✅ MIDI файл беше създаден: {output_path}")
    print(f"   Размер: {len(midi_data)} байта")
    print("\n🎵 Можете да отворите този файл с:")
    print("   - Windows Media Player")
    print("   - VLC")
    print("   - MuseScore")
    print("   - Audacity (за импортиране)")
    print("\n💡 За да конвертирате в MP3:")
    print("   1. Отворете в Audacity")
    print("   2. Файл → Импортирай → Audio")
    print("   3. Файл → Експортирай → MP3")


if __name__ == '__main__':
    main()
