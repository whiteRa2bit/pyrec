import typing as tp
from collections import defaultdict
import pyrec.processing.operations as ops

TRow = tp.Dict[str, tp.Any]
TRowsIterable = tp.Iterable[TRow]
TRowsGenerator = tp.Generator[TRow, None, None]


class HistoryReducer(ops.Reducer):
    def __init__(self, actions: TRowsIterable, id_column: str, to_id_column: str, timestamp_column: str,
                 history_column: str):
        self.actions = actions
        self.id_column = id_column
        self.to_id_column = to_id_column
        self.timestamp_column = timestamp_column
        self.history_column = history_column
        self.history = self._calculate_history()

    def _calculate_history(self):
        history = defaultdict(list)  # A    dd type
        for action in self.actions:  # Check that actions are sorted by ascending timestamp
            id = action[self.id_column]
            to_id = action[self.to_id_column]
            timestamp = action[self.timestamp_column]
            history[id].append({'to_id': to_id, 'timestamp': timestamp})
        return history

    def __call__(self, group_key: tp.Tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        for row in rows:
            result_row = {self.id_column: row[self.id_column], self.history_column: self.history[row[self.id_column]]}
            yield result_row
            break
