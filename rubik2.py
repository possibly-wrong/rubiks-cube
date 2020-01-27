import numpy as np
from collections import deque

def rankperm(p):
    """Return rank in [0, n!) of given permutation of range(n).

    W. Myrvold and F. Ruskey, Ranking and Unranking Permutations in
    Linear Time. Information Processing Letters, 79 (2001):281-284.
    """
    p = np.array(p)
    q = np.array(p).argsort()
    r = 0
    for k in range(len(p) - 1, 0, -1):
        s = p[k]
        p[k], p[q[k]] = p[q[k]], p[k]
        q[k], q[s] = q[s], q[k]
        r += s * np.math.factorial(k)
    return r

def unrankperm(r, n):
    """Return permutation of range(n) with given rank.

    W. Myrvold and F. Ruskey, Ranking and Unranking Permutations in
    Linear Time. Information Processing Letters, 79 (2001):281-284.
    """
    p = list(range(n))
    for k in range(n - 1, 0, -1):
        s, r = divmod(r, np.math.factorial(k))
        p[k], p[s] = p[s], p[k]
    return p

def packcube(cube):
    """Return integer index in range(7! * 3^6) of given cube state.
    """
    p, q = cube
    return rankperm(p) * 3**6 + sum(q[:6] * (3 ** np.arange(5, -1, -1)))

def unpackcube(i):
    """Return cube state with given integer index in range(7! * 3^6).
    """
    p, q = divmod(i, 3**6)
    q = np.array(list(map(ord, np.base_repr(q, 3, 6)[-6:]))) - ord('0')
    return (np.array(unrankperm(p, 7)), np.append(q, -sum(q) % 3))

# Cube moves are rotations X+, X-, Y+, Y-, Z+, Z-.
cubemoves = (
    (np.array([4, 1, 0, 3, 6, 5, 2]), np.array([0, 0, 0, 0, 0, 0, 0])),
    (np.array([2, 1, 6, 3, 0, 5, 4]), np.array([0, 0, 0, 0, 0, 0, 0])),
    (np.array([0, 2, 6, 3, 4, 1, 5]), np.array([0, 2, 1, 0, 0, 1, 2])),
    (np.array([0, 5, 1, 3, 4, 6, 2]), np.array([0, 2, 1, 0, 0, 1, 2])),
    (np.array([0, 1, 2, 5, 3, 6, 4]), np.array([0, 0, 0, 1, 2, 2, 1])),
    (np.array([0, 1, 2, 4, 6, 3, 5]), np.array([0, 0, 0, 1, 2, 2, 1])))

def movecube(cube, move):
    """Apply move to cube and return new cube state.
    """
    (cp, cq), (mp, mq) = cube, move
    return (cp[mp], (cq[mp] + mq) % 3)

def cubegraph():
    """Return adjacency list representation of cube graph.

    Each element g[v][m] of the (7! * 3^6) x 6 array indicates the index
    of the cube state reached from state v by move m.
    """
    n = np.math.factorial(7) * 3**6
    g = []
    for i in range(n):
        cube = unpackcube(i)
        g.append([packcube(movecube(cube, move)) for move in cubemoves])
    return g

def bfs(g, v):
    """Breadth-first search.

    Given an adjacency list representation of graph g and index of
    source vertex v, returns (p, d), where p is a predecessor vector
    representation of the shortest path spanning tree rooted at v, and d
    is a vector of corresponding path lengths from v to each vertex.
    """
    p = [-1] * len(g)
    d = [-1] * len(g)
    d[v] = 0
    q = deque([v])
    while q:
        v = q.popleft()
        for w in g[v]:
            if d[w] == -1:
                d[w] = d[v] + 1
                p[w] = v
                q.append(w)
    return (p, d)
