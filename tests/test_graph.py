import pytest

from exceptions import (
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    InvalidWeightError,
    PathNotFoundError,
    VertexAlreadyExistsError,
    VertexNotFoundError,
)
from graph import WeightedGraph


def test_add_vertex_increases_vertex_count() -> None:
    graph = WeightedGraph()

    graph.add_vertex("A")

    assert graph.vertex_count == 1


def test_add_existing_vertex_raises_error() -> None:
    graph = WeightedGraph()
    graph.add_vertex("A")

    with pytest.raises(VertexAlreadyExistsError, match="A"):
        graph.add_vertex("A")


def test_remove_vertex_removes_connected_edges() -> None:
    graph = _graph_with_vertices("A", "B")
    graph.add_edge("A", "B", 2.0)

    graph.remove_vertex("B")
    graph.add_vertex("B")
    expected_time = 3.0
    graph.add_edge("A", "B", expected_time)

    assert graph.shortest_time("A", "B") == expected_time


def test_remove_missing_vertex_raises_error() -> None:
    graph = WeightedGraph()

    with pytest.raises(VertexNotFoundError, match="A"):
        graph.remove_vertex("A")


def test_add_edge_connects_vertices_in_both_directions() -> None:
    graph = _graph_with_vertices("A", "B")
    expected_time = 2.5

    graph.add_edge("A", "B", expected_time)

    assert graph.shortest_time("A", "B") == expected_time
    assert graph.shortest_time("B", "A") == expected_time


@pytest.mark.parametrize("weight", [0.0, -1.0])
def test_add_edge_rejects_non_positive_weight(weight: float) -> None:
    graph = _graph_with_vertices("A", "B")

    with pytest.raises(InvalidWeightError, match=str(weight)):
        graph.add_edge("A", "B", weight)


def test_add_existing_edge_raises_error() -> None:
    graph = _graph_with_vertices("A", "B")
    graph.add_edge("A", "B", 1.0)

    with pytest.raises(EdgeAlreadyExistsError, match="A"):
        graph.add_edge("B", "A", 1.0)


def test_remove_edge_disconnects_vertices() -> None:
    graph = _graph_with_vertices("A", "B")
    graph.add_edge("A", "B", 1.0)

    graph.remove_edge("A", "B")

    with pytest.raises(PathNotFoundError):
        graph.shortest_time("A", "B")


def test_remove_missing_edge_raises_error() -> None:
    graph = _graph_with_vertices("A", "B")

    with pytest.raises(EdgeNotFoundError, match="A"):
        graph.remove_edge("A", "B")


@pytest.mark.parametrize(
    ("start", "end", "expected"),
    [("A", "D", 4.0), ("D", "A", 4.0), ("B", "D", 3.0)],
)
def test_shortest_time_chooses_best_route(
    start: str,
    end: str,
    expected: float,
) -> None:
    graph = _create_route_graph()

    result = graph.shortest_time(start, end)

    assert result == expected


def test_shortest_time_rejects_unknown_vertex() -> None:
    graph = _graph_with_vertices("A", "B")

    with pytest.raises(VertexNotFoundError, match="X"):
        graph.shortest_time("X", "B")


def test_shortest_path_restores_vertices_in_order() -> None:
    graph = _create_route_graph()

    path = graph.shortest_path("A", "D")

    assert path == ["A", "B", "C", "D"]


def test_shortest_path_to_same_vertex_contains_one_vertex() -> None:
    graph = _graph_with_vertices("A")

    path = graph.shortest_path("A", "A")

    assert path == ["A"]


def _graph_with_vertices(*vertices: str) -> WeightedGraph:
    graph = WeightedGraph()
    for vertex in vertices:
        graph.add_vertex(vertex)
    return graph


def _create_route_graph() -> WeightedGraph:
    graph = _graph_with_vertices("A", "B", "C", "D")
    graph.add_edge("A", "B", 1.0)
    graph.add_edge("B", "C", 1.0)
    graph.add_edge("C", "D", 2.0)
    graph.add_edge("A", "D", 10.0)
    graph.add_edge("B", "D", 5.0)
    return graph
