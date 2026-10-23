"""Взвешенный неориентированный граф и алгоритм Дейкстры."""

import heapq
import math

from exceptions import (
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    InvalidWeightError,
    PathNotFoundError,
    VertexAlreadyExistsError,
    VertexNotFoundError,
)


class WeightedGraph:
    """Взвешенный неориентированный граф со строковыми вершинами."""

    def __init__(self) -> None:
        """Создать пустой граф."""
        self._adjacency: dict[str, dict[str, float]] = {}

    @property
    def vertex_count(self) -> int:
        """Вернуть количество вершин графа."""
        return len(self._adjacency)

    def add_vertex(self, vertex: str) -> None:
        """Добавить новую вершину в граф."""
        if vertex in self._adjacency:
            raise VertexAlreadyExistsError(vertex)
        self._adjacency[vertex] = {}

    def remove_vertex(self, vertex: str) -> None:
        """Удалить вершину вместе со всеми связанными рёбрами."""
        self._check_vertex(vertex)
        for neighbour in self._adjacency[vertex]:
            del self._adjacency[neighbour][vertex]
        del self._adjacency[vertex]

    def add_edge(self, start: str, end: str, weight: float) -> None:
        """Добавить неориентированное ребро с положительным весом."""
        self._check_vertex(start)
        self._check_vertex(end)
        if weight <= 0:
            raise InvalidWeightError(weight)
        if end in self._adjacency[start]:
            raise EdgeAlreadyExistsError(start, end)
        self._adjacency[start][end] = weight
        self._adjacency[end][start] = weight

    def remove_edge(self, start: str, end: str) -> None:
        """Удалить неориентированное ребро."""
        self._check_vertex(start)
        self._check_vertex(end)
        if end not in self._adjacency[start]:
            raise EdgeNotFoundError(start, end)
        del self._adjacency[start][end]
        del self._adjacency[end][start]

    def shortest_time(self, start: str, end: str) -> float:
        """Вернуть вес кратчайшего пути между двумя вершинами."""
        distances, _ = self._dijkstra(start, end)
        return distances[end]

    def shortest_path(self, start: str, end: str) -> list[str]:
        """Вернуть вершины кратчайшего пути от начала до конца."""
        _, previous = self._dijkstra(start, end)
        path = [end]
        current = end

        while current != start:
            current = previous[current]
            path.append(current)
        path.reverse()
        return path

    def _check_vertex(self, vertex: str) -> None:
        if vertex not in self._adjacency:
            raise VertexNotFoundError(vertex)

    def _dijkstra(
        self,
        start: str,
        end: str,
    ) -> tuple[dict[str, float], dict[str, str]]:
        self._check_vertex(start)
        self._check_vertex(end)
        distances = dict.fromkeys(self._adjacency, math.inf)
        distances[start] = 0.0
        previous: dict[str, str] = {}
        queue = [(0.0, start)]
        visited: set[str] = set()

        while queue:
            current_distance, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            if current == end:
                return distances, previous
            for neighbour, weight in self._adjacency[current].items():
                new_distance = current_distance + weight
                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    previous[neighbour] = current
                    heapq.heappush(queue, (new_distance, neighbour))

        raise PathNotFoundError(start, end)
