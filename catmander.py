#/bin/python

# This code works with the Kittenbot Meowbit.
#
# The Meowbit generates MIDI signals and sends them via a UART line to a MIDI
# device.
# 
# It assumes the following circuit:
#   PIN9 --> DIN5
#   3.3V --> 220ohm --> DIN4

# Timer comes from the meowbit module
# from machine import Timer
from meowbit import *

import micropython

import random

sequence = [[0, 0, 0, 0_0, 0, 0, 0, 0_0],
            [0, 0, 0, 0_0, 0, 0, 0, 0_0],
            [0, 0, 0, 0_0, 0, 0, 0, 0_0],
            [0, 0, 0, 0_0, 0, 0, 0, 0_0],
            [0, 0, 0, 0_0, 0, 0, 0, 0_0],
            [0, 0, 0, 0_0, 0, 0, 0, 0_0],
            [0, 0, 0, 0_0, 0, 0, 0, 0_0],
            [0, 0, 0, 0_0, 0, 0, 0, 0_0]]

root_note = 45

note_delta = [0, 4, 7, 9, 12, 16, 19, 22]

sequence_ptr = 0

midi = UART(6, 31250)

def draw_sequence():
    global sequence
    global sequence_ptr
    screen.fill((100, 100, 100))
    screen.rect(sequence_ptr * 20, 0, 20, 8 * 15, color=0, fill=1)
    for i, r in enumerate(sequence):
        for j, c in enumerate(r):
            screen.text(hex(c)[2:], j * 20, i * 15, color = (255, 0, 0))
    screen.refresh()

def noteon(note, velocity, channel = 0):
    b1 = (0b10010000) | (channel & 0x0F) 
    b2 = note & 0xFF
    b3 = velocity & 0xFF
    return bytes([b1, b2, b3])

def onBtnaPressed():
    global sequence
    for _ in range(0, random.randint(0, 32)):
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        print(i, j)
        sequence[i][j] = 0
    draw_sequence()

def onBtnbPressed():
    global sequence
    for _ in range(0, random.randint(0, 32)):
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        print(i, j)
        velocity = random.randint(-32, 127)
        sequence[i][j] = max(velocity, -1)
    draw_sequence()

def play_note(arg):
    global sequence
    global root_note
    global note_delta
    global sequence_ptr

    for i, r in enumerate(sequence):
        velocity = r[sequence_ptr]
        if velocity > -1:
            note = root_note + note_delta[i]
            midi.write(noteon(note, 0))

    sequence_ptr = (sequence_ptr + 1) % len(sequence[0])

    for i, r in enumerate(sequence):
        velocity = r[sequence_ptr]
        if velocity > -1:
            note = root_note + note_delta[i]
            midi.write(noteon(note, velocity))

    draw_sequence()

def on_tick(t):
    micropython.schedule(play_note, None)

sensor.btnTrig['a']=onBtnaPressed
sensor.btnTrig['b']=onBtnbPressed

sensor.startSchedule()

timer = Timer(1)

timer.init(period=250, callback=on_tick)

screen.sync = 0

draw_sequence()
