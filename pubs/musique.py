"""Compose la musique de la pub FacturePrête (20,5 s, calme, 84 BPM) -> musique.wav.

Nappe chaude Fa7M - Mi m7 - Ré m7 - Do7M, arpège pincé, basse douce, percussions
légères, et petits carillons calés sur les moments clés de la vidéo.
"""
import sys
import wave
import numpy as np

SR = 44100
DUR = 20.5
BPM = 84
BEAT = 60 / BPM
BAR = 4 * BEAT
N = int(SR * DUR)
rng = np.random.default_rng(7)


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e


def add(buf, sig, t, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(sig), 0] += sig * l
    buf[i:i + len(sig), 1] += sig * r


def pad_note(f, dur):
    t = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * d * t) for d in (0.997, 1.0, 1.003)) / 3
    s += 0.25 * np.sin(2 * np.pi * 2 * f * t) + 0.08 * np.sin(2 * np.pi * 3 * f * t)
    return s * env(len(t), 0.8, 0.9) * 0.06


def pluck(f, dur=1.2):
    n = int(dur * SR); p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p); out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * env(n, 0.002, 0.3) * 0.12


def bass(f, dur):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)) * env(len(t), 0.02, 0.4) * 0.16


def kick():
    t = np.arange(int(0.35 * SR)) / SR
    f = 110 * np.exp(-t * 18) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.22


def shaker():
    n = int(0.08 * SR); s = rng.uniform(-1, 1, n)
    s = np.diff(np.concatenate([[0], s]))  # brighter
    return s * np.exp(-np.arange(n) / SR * 60) * 0.025


def chime(f):
    t = np.arange(int(1.4 * SR)) / SR
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 6)
    return s * np.exp(-t * 3.2) * 0.10


def whoosh():
    n = int(0.7 * SR); s = rng.normal(0, 1, n)
    k = np.ones(40) / 40; s = np.convolve(s, k, "same")
    return s * np.sin(np.linspace(0, np.pi, n)) ** 2 * 0.05


CHORDS = [  # (root midi, chord tones)
    (41, [53, 57, 60, 64]),  # Fmaj7
    (40, [52, 55, 59, 62]),  # Em7
    (38, [50, 53, 57, 60]),  # Dm7
    (36, [48, 52, 55, 59]),  # Cmaj7
]

out = np.zeros((N, 2))
bar, t = 0, 0.0
while t < DUR:
    root, tones = CHORDS[bar % 4]
    for k, m in enumerate(tones):
        add(out, pad_note(midi(m), BAR + 0.6), t, pan=(-0.4 + 0.27 * k))
    add(out, bass(midi(root), BAR * 0.95), t)
    arp = tones + [tones[1] + 12, tones[2] + 12, tones[3] + 12, tones[2] + 12]
    if bar >= 1:
        for i, m in enumerate(arp):
            add(out, pluck(midi(m + 12)), t + i * BEAT / 2, pan=0.35 if i % 2 else -0.35)
    if bar >= 2:
        for b in (0, 2):
            add(out, kick(), t + b * BEAT)
        for b in range(8):
            if b % 2: add(out, shaker(), t + b * BEAT / 2, pan=0.5)
    t += BAR; bar += 1

for ts in (4.3, 9.3, 15.0):
    add(out, whoosh(), ts - 0.35)
for ts, m in ((12.2, 84), (12.7, 88), (13.2, 91)):
    add(out, chime(midi(m)), ts, pan=0.1)
add(out, chime(midi(96)) * 0.8, 15.2)

fade = env(N, 1.0, 1.8)
out *= fade[:, None]
out /= max(1e-9, np.abs(out).max()) / 0.9
with wave.open(sys.argv[1] if len(sys.argv) > 1 else "musique.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype("<i2").tobytes())
