#!/usr/bin/env python3
"""Procedural noise: Perlin, value noise, and Worley."""
import sys, math, random

def lerp(a, b, t): return a + t*(b-a)
def fade(t): return t*t*t*(t*(t*6-15)+10)

class PerlinNoise:
    def __init__(self, seed=42):
        random.seed(seed)
        self.p = list(range(256)); random.shuffle(self.p); self.p *= 2
        self.grads = [(math.cos(a),math.sin(a)) for a in [random.uniform(0,2*math.pi) for _ in range(256)]]
    def _grad(self, h, x, y):
        g = self.grads[h & 255]; return g[0]*x + g[1]*y
    def noise(self, x, y):
        xi, yi = int(math.floor(x)) & 255, int(math.floor(y)) & 255
        xf, yf = x - math.floor(x), y - math.floor(y)
        u, v = fade(xf), fade(yf)
        aa = self.p[self.p[xi]+yi]; ab = self.p[self.p[xi]+yi+1]
        ba = self.p[self.p[xi+1]+yi]; bb = self.p[self.p[xi+1]+yi+1]
        x1 = lerp(self._grad(aa,xf,yf), self._grad(ba,xf-1,yf), u)
        x2 = lerp(self._grad(ab,xf,yf-1), self._grad(bb,xf-1,yf-1), u)
        return lerp(x1, x2, v)
    def fbm(self, x, y, octaves=4, lacunarity=2, gain=0.5):
        total = 0; amp = 1; freq = 1; max_val = 0
        for _ in range(octaves):
            total += self.noise(x*freq, y*freq)*amp
            max_val += amp; amp *= gain; freq *= lacunarity
        return total/max_val

def main():
    pn = PerlinNoise(42); chars = " ·░▒▓█"
    print("Perlin noise (FBM, 4 octaves):")
    for y in range(20):
        row = ""
        for x in range(60):
            v = (pn.fbm(x*0.05, y*0.1) + 1) / 2
            row += chars[min(int(v*6), 5)]
        print(row)

if __name__ == "__main__": main()
