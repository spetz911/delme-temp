import sys


def recover_path(path, n, step, i, j):
    """ Use paths matrix to recover negative cycle """
    ans = [0] * (step + 1)
    ans[step] = i+1
    while step:
        ans[step-1] = path[i][j][step] + 1
        j = path[i][j][step]
        step -= 1
    return ans + [j+1]


def resolve_internal(g, path):
    """ Floyd-Warshall algorithm with 3rd dim and path recovering """
    n = len(g)
    for step in range(1, n):
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    cost = g[i][k][step-1] * g[k][j][0]
                    if g[i][j][step] < cost:
                        g[i][j][step] = cost
                        path[i][j][step] = k
                        if i == j and g[i][i][step] > 1.01:
                            return recover_path(path, n, step, i, j)
    return None


def solve(matrix):
    """ Adds thind dimension to graph edges """
    n = len(matrix)
    assert n > 0
    assert len(matrix[0]) == n
    # create 3d matrix
    path = list(list(list(-1
                for _ in range(n))
            for _ in range(n))
        for _ in range(n))
    graph = list(list(list(0.0
                for _ in range(n))
            for _ in range(n))
        for _ in range(n))
    for i in range(n):
        for j in range(n):
            graph[i][j][0] = matrix[i][j]
            path[i][j][0] = i
    return resolve_internal(graph, path)


def main():
    """ Need to check uva.onlinejudge.org 104 - Arbitrage AC """
    while True:
        s = sys.stdin.readline()
        if not s:
            break
        n = int(s.strip())
        matrix = list([0.0] * n for _ in range(n))
        for i in range(n):
            tmp = list(map(float, sys.stdin.readline().split()))
            tmp.insert(i, 1.0)
            matrix[i] = tmp
        res = solve(matrix)
        if res:
            print(*res, sep=' ')
        else:
            print("no arbitrage sequence exists")


if __name__ == '__main__':
    main()

