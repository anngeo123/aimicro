
import streamlit as st
import sqlite3
import heapq
import math

conn = sqlite3.connect("school.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    x REAL,
    y REAL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS paths (
    start_id INTEGER,
    end_id INTEGER,
    distance REAL,
    PRIMARY KEY (start_id, end_id)
)
""")

count = conn.execute(
    "SELECT COUNT(*) FROM locations"
).fetchone()[0]

if count == 0:
    locations = [
        (1, "Main Gate", 0, 0),
        (2, "Block A", 2, 0),
        (3, "AI Lab", 5, 0),
        (4, "Computer Lab", 2, 2),
        (5, "Library", 5, 2),
        (6, "Canteen", 0, 4)
    ]

    paths = [
        (1, 2, 2),
        (1, 6, 4),
        (2, 3, 3),
        (2, 4, 2),
        (4, 5, 3)
    ]

    conn.executemany(
        "INSERT INTO locations VALUES (?, ?, ?, ?)",
        locations
    )

    conn.executemany(
        "INSERT INTO paths VALUES (?, ?, ?)",
        paths
    )

    conn.commit()

rows = conn.execute(
    "SELECT id, name, x, y FROM locations"
).fetchall()

names = {row[0]: row[1] for row in rows}

coordinates = {
    row[0]: (row[2], row[3]) for row in rows
}

graph = {location_id: {} for location_id in names}

edges = conn.execute(
    "SELECT start_id, end_id, distance FROM paths"
).fetchall()

for start, end, distance in edges:
    graph[start][end] = distance
    graph[end][start] = distance

conn.close()


def astar(start, goal):

    def heuristic(node):
        x1, y1 = coordinates[node]
        x2, y2 = coordinates[goal]

        return math.sqrt(
            (x1 - x2) ** 2 + (y1 - y2) ** 2
        )

    queue = [(heuristic(start), start)]
    distance = {start: 0}
    path = {start: None}

    while queue:
        f, current = heapq.heappop(queue)

        if current == goal:
            break

        for neighbour, cost in graph[current].items():
            new_distance = distance[current] + cost

            if (
                neighbour not in distance
                or new_distance < distance[neighbour]
            ):
                distance[neighbour] = new_distance
                path[neighbour] = current

                f = new_distance + heuristic(neighbour)

                heapq.heappush(queue, (f, neighbour))

    if goal not in path:
        return None, None

    route = []
    current = goal

    while current is not None:
        route.append(current)
        current = path[current]

    route.reverse()

    return [names[node] for node in route], distance[goal]


st.title("🏫 Smart School Navigator")

st.write(
    "Find the shortest route between school locations using A* Search."
)

location_ids = list(names.keys())

start = st.selectbox(
    "Starting Point",
    location_ids,
    format_func=lambda x: names[x]
)

destination = st.selectbox(
    "Destination",
    location_ids,
    format_func=lambda x: names[x]
)

if st.button("🔍 Find Route"):

    if start == destination:
        st.warning(
            "Starting point and destination are the same."
        )

    else:
        route, total_distance = astar(start, destination)

        if route is not None:
            st.success("Route Found!")

            st.write("### 📍 Shortest Route")
            st.write(" → ".join(route))

            st.write(
                f"### 📏 Distance: {total_distance} units"
            )

            st.write("### 🧠 How A* works")

            st.write(
                "A* combines the distance already travelled (g) "
                "with an estimated distance remaining (h)."
            )

        else:
            st.error("No route found.")

st.caption(
    "Currently using example school data stored in SQLite."
)
