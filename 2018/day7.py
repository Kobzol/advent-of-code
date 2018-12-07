from heapq import heappop, heappush

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]

graph = {}
for line in lines:
    line = line.split(" ")
    src = ord(line[1]) - ord('A')
    dest = ord(line[7]) - ord('A')
    graph.setdefault(src, []).append(dest)
    graph.setdefault(dest, [])

graph_in = {}
for n in graph:
    graph_in.setdefault(n, [])
    for v in graph[n]:
        graph_in.setdefault(v, []).append(n)

workers = [0] * 5
planned = set()
finished = set()
events = []
ready = sorted([n for n in graph if n not in planned and all([v in planned for v in graph_in[n]])])
for r in ready:
    planned.add(r)
    events.append((0, r, "start"))


def length(task):
    return 60 + task + 1


while events:
    (time, task, event) = heappop(events)
    if event == "start":
        free_worker = [w for w in workers if w <= time]
        if not free_worker:
            heappush(events, (min(workers), task, "start"))
        else:
            for (i, w) in enumerate(workers):
                if w <= time:
                    workers[i] = time + length(task)
                    heappush(events, (time + length(task), task, "end"))
                    break
    elif event == "end":
        finished.add(task)
        ready = sorted([n for n in graph if n not in planned and all([v in finished for v in graph_in[n]])])
        for r in ready:
            events.append((time, r, "start"))
            planned.add(r)
        print(task, time)

print(workers)
