import random
import math


def dfs(indx, n, query, visited, set_color):
    visited[indx] = True
    set_color.append(indx)

    for i in range(n):
        if query[indx][i] == 1 and not visited[i]:
            dfs(i, n, query, visited, set_color)


def dfs_connected_groups(indx, n, query, visited, labels, excluded):
    visited[indx] = True

    for i in range(n):
        if query[indx][i] == 0:
            if (labels[indx], labels[i]) not in excluded and (labels[i], labels[indx]) not in excluded:
                excluded.append((labels[indx], labels[i]))
            if not visited[i]:
                dfs_connected_groups(i, n, query, visited, labels, excluded)


def non_connected_groups(n, query, sets_color, c, count):
    visited = list([False for _ in range(n)])
    excluded = []

    labels = {i: None for i in range(n)}
    for i in range(n):
        for j, s in enumerate(sets_color):
            if i in s:
                labels[i] = j

    included_question = lambda indx: len(
        list([True for j in range(n) if indx != j and (query[indx][j] == 0 or query[indx][j] == 1)])) > 0

    for i in range(n):
        if not visited[i] and included_question(i):
            dfs_connected_groups(i, n, query, visited, labels, excluded)

    if (len(sets_color) + 1) * (len(sets_color) + 1) // 2 >= n // 2 - count:
        for i in range(len(sets_color)):
            for j in range(i + 1, len(sets_color)):
                if not (i, j) in excluded and not (j, i) in excluded:
                    return random.choice(sets_color[i]), random.choice(sets_color[j])
    return None


def connected_components(n, query):
    visited = list([False for _ in range(n)])
    sets_color = []

    included_question = lambda indx: len(
        list([True for j in range(n) if indx != j and (query[indx][j] == 1 or query[indx][j] == 0)])) > 0

    for i in range(n):
        if not visited[i] and included_question(i):
            set_color = []
            dfs(i, n, query, visited, set_color)
            sets_color.append(set_color)

    # sets_color.sort(key=lambda s: len(s))
    # random.shuffle(sets_color)
    return sets_color, visited


def nextQuestion(n, ignore_1, ignore_2, c, ignore_3, query, pair_out=[]):
    for i in range(n):
        query[i][i] = -1
        for j in range(i + 1, n):
            if j not in query[i]:
                query[i][j] = -1
                query[j][i] = -1

    sets_color, visited = connected_components(n, query)
    non_visited = list([i for i, v in enumerate(visited) if not v])

    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if query[i][j] != -1:
                count += 1

    if len(sets_color) > 0 and count >= n // 2:
        pair = [(len(s), s, s[0]) for s in sets_color]
        _, max_set, r_ = max(pair, key=lambda e: e[0])
        calc = lambda pm, p: ((pm - p) / (math.sqrt(pm * p / (n - len(non_visited))))) > 2.6
        finish = True
        for l, s, r in pair:
            if 1 / (c - 1) > len(max_set) / (n - len(non_visited)):
                finish = False
                break
            elif r != r_ and len(s) > 0 and len(max_set) > 0 and n - len(non_visited) > 0:
                pm = len(max_set) / (n - len(non_visited))
                p = len(s) / (n - len(non_visited))
                if pm > 0 and p > 0:
                    f = calc(pm, p)
                    if not f:
                        finish = False
                        break
        # (K - 1) * (N - K/2)
        if (int((c - 1) * (n - c / 2)) >= count and finish):
            print("%d" % (random.choice(max_set)))
            return
        if count == int((c - 1) * (n - c / 2)):
            print("%d" % (random.choice(max_set)))
            return
        if len(non_visited) == 0:
            print("%d" % (random.choice(max_set)))
            return

    strong_connected = non_connected_groups(n, query, sets_color, c, count)

    if strong_connected is not None:
        i_, j_ = strong_connected
    else:
        if len(sets_color) == 0:
            i_ = random.choice(list([k for k in range(n)]))
            j_ = random.choice(list([k for k in range(n) if k != i_]))
        else:
            i_ = random.choice(random.choice(sets_color))
            j_ = random.choice(non_visited)
    print("%d %d" % (i_, j_))


if __name__ == '__main__':
    vals = [int(i) for i in raw_input().strip().split()]
    query_size = input()
    query = {}
    for i in range(vals[0]):
        query[i] = {}

    for i in range(query_size):
        temp = [j for j in raw_input().strip().split()]
        if temp[2] == "YES":
            query[int(temp[0])][int(temp[1])] = 1
            query[int(temp[1])][int(temp[0])] = 1
        else:
            query[int(temp[0])][int(temp[1])] = 0
            query[int(temp[1])][int(temp[0])] = 0

    nextQuestion(vals[0], vals[1], vals[2], vals[3], vals[4], query)