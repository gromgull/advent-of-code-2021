import numpy as np

# this one never worked. I didn't realise that most X velocities will cause the
# x movement to stop inside the target area, meaning the y movement can take as
# many timesteps as you want to reach the target

def solve(x,y):

    xs = np.arange(x[0], x[1]+1)
    print(xs)
    sol = (-1 + np.sqrt(1+8*xs)) / 2
    print(sol)

    vxs = sol[np.isclose(sol, np.around(sol))].astype(int) # integer solutions

    for t in range(2,200):
        print('t',t)
        t-=1

        ys = np.linspace(y[0],y[1], abs(y[0]-y[1])+1)
        sol = (ys+((t-1)**2+t-1)/2)/t
        print(sol)

        vy = np.floor(sol).max()
        print('vy', vy)
        t = np.arange(t)
        print('max height', (t*vy-((t-1)**2+t-1)/2).max())

solve([20, 30], [-10,-5])
print('-'*10)
solve([70, 125], [-159,-121])
