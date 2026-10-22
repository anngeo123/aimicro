import streamlit as st
import heapq

# School map
graph = {
    "Main Gate": {"Block A": 2, "Canteen": 4},
    "Block A": {"Main Gate": 2, "AI Lab": 3, "Computer Lab": 2},
    "AI Lab": {"Block A": 3},
    "Computer Lab": {"Block A": 2, "Library": 3},
    "Library": {"Computer Lab": 3},
    "Canteen": {"Main Gate": 4}
}

# Approximate heuristic values
heuristic = {
    "Main Gate": 5,
    "Block A": 3,
    "AI Lab": 0,
    "Computer Lab": 2,
    "Library": 4,
    "Canteen": 5
}

def astar(start, goal):
    queue = [(0, start)]
    distance = {start: 0}
    path = {start: None}

    while queue:
        current_cost, current = heapq.heappop(queue)

        if current == goal:
            break

        for neighbour, cost in graph[current].items():
            new_distance = distance[current] + cost

            if neighbour not in distance or new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                path[neighbour] = current

                f = new_distance + heuristic[neighbour]
                heapq.heappush(queue, (f, neighbour))

    if goal not in path:
        return None, None

    route = []
    current = goal

    while current is not None:
        route.append(current)
        current = path[current]

    route.reverse()

    return route, distance[goal]


# Interface
st.title("🏫 Smart School Navigator")
st.write("Find the shortest route between locations using A* Search.")

locations = list(graph.keys())

start = st.selectbox("Starting Point", locations)
destination = st.selectbox("Destination", locations)

if st.button("🔍 Find Route"):

    if start == destination:
        st.warning("Starting point and destination are the same.")

    else:
        route, distance = astar(start, destination)

        if route:
            st.success("Route Found!")

            st.write("### 📍 Shortest Route")

            st.write(" → ".join(route))

            st.write(f"### 📏 Distance: {distance} units")

            st.write("### 🧠 A* Search")
            st.write(
                "A* combines the distance already travelled "
                "(g) with an estimated distance to the destination (h)."
            )

        else:
            st.error("No route found.")