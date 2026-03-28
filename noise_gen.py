#!/usr/bin/env python3
"""noise_gen - Value noise and Perlin-like noise."""
import sys, math, random, hashlib
def value_noise_1d(x, seed=0):
    def hash_int(n):
        return int(hashlib.md5(f"{n}:{seed}".encode()).hexdigest()[:8],16)/0xFFFFFFFF
    x0=int(math.floor(x)); x1=x0+1; t=x-x0
    t=t*t*(3-2*t)  # smoothstep
    return hash_int(x0)*(1-t)+hash_int(x1)*t
def value_noise_2d(x, y, seed=0):
    def hash_2d(ix, iy):
        return int(hashlib.md5(f"{ix},{iy}:{seed}".encode()).hexdigest()[:8],16)/0xFFFFFFFF
    x0,y0=int(math.floor(x)),int(math.floor(y)); x1,y1=x0+1,y0+1
    tx,ty=x-x0,y-y0; tx=tx*tx*(3-2*tx); ty=ty*ty*(3-2*ty)
    c00,c10,c01,c11=hash_2d(x0,y0),hash_2d(x1,y0),hash_2d(x0,y1),hash_2d(x1,y1)
    return (c00*(1-tx)+c10*tx)*(1-ty)+(c01*(1-tx)+c11*tx)*ty
def fbm(x, y, octaves=4, lacunarity=2.0, gain=0.5, seed=0):
    total=0; amplitude=1; frequency=1; max_val=0
    for _ in range(octaves):
        total+=value_noise_2d(x*frequency,y*frequency,seed)*amplitude
        max_val+=amplitude; amplitude*=gain; frequency*=lacunarity
    return total/max_val
if __name__=="__main__":
    w,h=60,25; scale=float(sys.argv[1]) if len(sys.argv)>1 else 0.1
    chars=" .:-=+*#%@"
    for r in range(h):
        line=""
        for c in range(w):
            v=fbm(c*scale,r*scale,octaves=4)
            line+=chars[int(v*(len(chars)-1))]
        print(line)
