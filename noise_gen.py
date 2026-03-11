#!/usr/bin/env python3
"""Noise generator — Perlin, Simplex, and Worley noise."""
import sys, math, random

def _fade(t): return t*t*t*(t*(t*6-15)+10)
def _lerp(a, b, t): return a + t*(b-a)

class PerlinNoise:
    def __init__(self, seed=0):
        random.seed(seed)
        self.p = list(range(256)); random.shuffle(self.p); self.p *= 2
        self.g = [(math.cos(a), math.sin(a)) for a in (random.uniform(0, 2*math.pi) for _ in range(256))]
    def _grad(self, h, x, y):
        g = self.g[h & 255]
        return g[0]*x + g[1]*y
    def noise(self, x, y):
        xi, yi = int(x) & 255, int(y) & 255
        xf, yf = x - int(x), y - int(y)
        u, v = _fade(xf), _fade(yf)
        p = self.p
        aa, ab = p[p[xi]+yi], p[p[xi]+yi+1]
        ba, bb = p[p[xi+1]+yi], p[p[xi+1]+yi+1]
        return _lerp(_lerp(self._grad(aa, xf, yf), self._grad(ba, xf-1, yf), u),
                     _lerp(self._grad(ab, xf, yf-1), self._grad(bb, xf-1, yf-1), u), v)
    def octave(self, x, y, octaves=4, persistence=0.5):
        total = 0; amp = 1; freq = 1; max_val = 0
        for _ in range(octaves):
            total += self.noise(x*freq, y*freq) * amp
            max_val += amp; amp *= persistence; freq *= 2
        return total / max_val

if __name__ == "__main__":
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
    pn = PerlinNoise(42)
    chars = " ░▒▓█"
    for y in range(h):
        row = ""
        for x in range(w):
            v = (pn.octave(x*scale, y*scale, 6) + 1) / 2
            idx = min(len(chars)-1, int(v * len(chars)))
            row += chars[idx]
        print(row)
