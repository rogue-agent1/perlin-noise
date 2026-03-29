import argparse, math, random

def fade(t): return t*t*t*(t*(t*6-15)+10)
def lerp(a, b, t): return a + t*(b-a)

def perlin_2d(width, height, scale=10, octaves=4, seed=None):
    if seed: random.seed(seed)
    # Generate gradient grid
    gw, gh = width//scale+2, height//scale+2
    grads = [[(random.gauss(0,1), random.gauss(0,1)) for _ in range(gw)] for _ in range(gh)]
    def dot_grad(ix, iy, x, y):
        dx, dy = x-ix, y-iy
        gx, gy = grads[iy % gh][ix % gw]
        return dx*gx + dy*gy
    def noise(x, y):
        x0, y0 = int(x), int(y)
        x1, y1 = x0+1, y0+1
        sx, sy = fade(x-x0), fade(y-y0)
        n0 = lerp(dot_grad(x0,y0,x,y), dot_grad(x1,y0,x,y), sx)
        n1 = lerp(dot_grad(x0,y1,x,y), dot_grad(x1,y1,x,y), sx)
        return lerp(n0, n1, sy)
    grid = [[0.0]*width for _ in range(height)]
    for o in range(octaves):
        freq = 2**o
        amp = 0.5**o
        for y in range(height):
            for x in range(width):
                grid[y][x] += noise(x*freq/scale, y*freq/scale) * amp
    return grid

def main():
    p = argparse.ArgumentParser(description="Perlin noise generator")
    p.add_argument("-w", "--width", type=int, default=60)
    p.add_argument("-H", "--height", type=int, default=30)
    p.add_argument("-s", "--scale", type=int, default=10)
    p.add_argument("-o", "--octaves", type=int, default=4)
    p.add_argument("--seed", type=int)
    args = p.parse_args()
    grid = perlin_2d(args.width, args.height, args.scale, args.octaves, args.seed)
    chars = " ·:;+*#%@"
    mn = min(min(r) for r in grid)
    mx = max(max(r) for r in grid)
    rng = mx - mn or 1
    for row in grid:
        print("".join(chars[min(int((v-mn)/rng*(len(chars)-1)), len(chars)-1)] for v in row))

if __name__ == "__main__":
    main()
