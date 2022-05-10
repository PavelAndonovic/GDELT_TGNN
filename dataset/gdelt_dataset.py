import pickle
import numpy as np
from torch_geometric_temporal.signal import DynamicGraphTemporalSignal


class GDELTDatasetLoader(object):

    def __init__(
        self,
        data_path,
        time_periods=None
    ):
        self._read_data(data_path)
        if time_periods:
            self._time_periods = time_periods

    def _read_data(self, data_path):
        with open(data_path, 'rb') as f:
            self._dataset = pickle.load(f)

    def _get_edges(self):
        self.edges = []
        if hasattr(self, '_time_periods'):
            tp = self._time_periods
        else:
            tp = self._dataset["time_periods"]
        for time in range(tp):
            E = np.array(self._dataset[str(time)]["edges"])
            self.edges.append(E.T)

    def _get_edge_weights(self):
        self.edge_weights = []
        if hasattr(self, '_time_periods'):
            tp = self._time_periods
        else:
            tp = self._dataset["time_periods"]
        for i, time in enumerate(range(tp)):
            W = np.array(self._dataset[str(time)]["weights"])
            W = np.divide(W, 100)
            self.edge_weights.append(W)

    def _get_features(self):
        self.features = []
        if hasattr(self, '_time_periods'):
            tp = self._time_periods
        else:
            tp = self._dataset["time_periods"]
        for time in range(tp):
            X = np.array(self._dataset[str(time)]["X"])
            X = np.divide(X, 100)
            self.features.append(X)

    def _get_targets(self):
        self.targets = []
        if hasattr(self, '_time_periods'):
            tp = self._time_periods
        else:
            tp = self._dataset["time_periods"]
        for time in range(tp):
            y = np.array(self._dataset[str(time)]["y"])
            self.targets.append(y)

    def get_dataset(self) -> DynamicGraphTemporalSignal:
        """Returning the TennisDataset data iterator.
        Return types:
            * **dataset** *(DynamicGraphTemporalSignal)*
        """
        self._get_edges()
        self._get_edge_weights()
        self._get_features()
        self._get_targets()
        dataset = DynamicGraphTemporalSignal(
            self.edges, self.edge_weights, self.features, self.targets
        )
        return dataset