from metro_data import build_metro_graph


def test_metro_has_at_least_thirty_stations() -> None:
    graph = build_metro_graph()
    minimum_station_count = 30

    station_count = graph.vertex_count

    assert station_count >= minimum_station_count


def test_metro_route_uses_transfer() -> None:
    graph = build_metro_graph()

    path = graph.shortest_path(
        "Арбатская (Арбатско-Покровская)",
        "Таганская (Кольцевая)",
    )

    assert "Курская (Арбатско-Покровская)" in path
    assert "Курская (Кольцевая)" in path
