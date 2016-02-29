
class Edge:
    def __init__(self, a,b,cost):
        self.a = a
        self.b = b
        self.cost = cost


INF = 1000000000;


def solve(edges, n):
    d = [0] * n
    p = [-1] * n
    for i in range(n):
        x = -1
        for j in range(len(edges)):
            if d[edges[j].b] > d[edges[j].a] + edges[j].cost:
                # FIXME -inf looks scary
                d[edges[j].b] = max(-INF, d[edges[j].a] + edges[j].cost)
                p[edges[j].b] = edges[j].a
                x = edges[j].b
    if x == -1:
        return None
    else:
        y = x
        for i in range(n):
            y = p[y]
        path = []
        cur = y
        while True:
            cur = p[cur]
            path.append(cur)
            if cur == y and len(path) > 1:
                break
        path.reverse()
        return path


def main():
    import sys
    import math

    while True:
        s = sys.stdin.readline()
        if not s:
            break
        # else
        edges = []
        n = int(s.strip())
        for i in range(n):
            row = list(map(float, sys.stdin.readline().split()))
            row.insert(i, 1.0)
            print "row = ", row
            for j in range(len(row)):
                cost = row[j]
                if i != j:
                    # FIXME log(0.0) should be checked
                    edges.append(Edge(i, j, -math.log(cost)))

        res = solve(edges, n)
        if res:
            for i in range(len(res)):
                print res[i] + 1,
            print res[0] + 1
        else:
            print("No negative cycle found.")



if __name__ == '__main__':
    main()




