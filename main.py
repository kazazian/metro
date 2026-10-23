"""Консольная утилита для поиска маршрутов в метро."""

import argparse
import sys

from exceptions import MetroGraphError
from metro_data import build_metro_graph


def create_parser() -> argparse.ArgumentParser:
    """Создать и настроить парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Поиск кратчайшего маршрута по Московскому метро.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    path_parser = subparsers.add_parser(
        "path",
        help="вывести станции кратчайшего маршрута",
    )
    _add_route_arguments(path_parser)

    time_parser = subparsers.add_parser(
        "time",
        help="вывести время кратчайшего маршрута",
    )
    _add_route_arguments(time_parser)
    return parser


def _add_route_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--from", dest="start", required=True, help="начальная станция")
    parser.add_argument("--to", dest="end", required=True, help="конечная станция")


def main(arguments: list[str] | None = None) -> int:
    """Выполнить выбранную команду и вернуть код завершения."""
    args = create_parser().parse_args(arguments)
    command = str(args.command)
    start = str(args.start)
    end = str(args.end)
    graph = build_metro_graph()

    try:
        if command == "time":
            print(f"{graph.shortest_time(start, end):g}")
        else:
            for station in graph.shortest_path(start, end):
                print(station)
    except MetroGraphError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
