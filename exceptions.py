"""Исключения для библиотеки взвешенного графа."""


class MetroGraphError(Exception):
    """Базовое исключение для всех ошибок графа."""


class VertexAlreadyExistsError(MetroGraphError):
    """Вершина уже существует в графе."""

    def __init__(self, vertex: str) -> None:
        super().__init__(f'вершина "{vertex}" уже существует')


class VertexNotFoundError(MetroGraphError):
    """Вершина не найдена в графе."""

    def __init__(self, vertex: str) -> None:
        super().__init__(f'вершина "{vertex}" не найдена')


class EdgeAlreadyExistsError(MetroGraphError):
    """Ребро уже существует в графе."""

    def __init__(self, start: str, end: str) -> None:
        super().__init__(f'ребро "{start}" - "{end}" уже существует')


class EdgeNotFoundError(MetroGraphError):
    """Ребро не найдено в графе."""

    def __init__(self, start: str, end: str) -> None:
        super().__init__(f'ребро "{start}" - "{end}" не найдено')


class InvalidWeightError(MetroGraphError):
    """Вес ребра не является положительным числом."""

    def __init__(self, weight: float) -> None:
        super().__init__(f"вес ребра должен быть положительным, получено: {weight}")


class PathNotFoundError(MetroGraphError):
    """Между двумя вершинами нет пути."""

    def __init__(self, start: str, end: str) -> None:
        super().__init__(f'путь от "{start}" до "{end}" не найден')
