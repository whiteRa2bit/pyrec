import typing as tp
from seqrec.processing.operations import Operation

TRow = tp.Dict[str, tp.Any]
TRowsIterable = tp.Iterable[TRow]
TRowsGenerator = tp.Generator[TRow, None, None]


class TargetRule(Operation):
    def __init__(self, target_column: str, min_target: float = float('-inf'), max_target: float = float('inf')):
        self.target_column = target_column
        self.min_target = min_target
        self.max_target = max_target

    def __call__(self, rows: TRowsIterable) -> TRowsGenerator:
        for row in rows:
            if self.min_target <= row[self.target_column] <= self.max_target:
                yield row
