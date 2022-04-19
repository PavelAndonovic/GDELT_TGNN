import torch
import torch.nn.functional as F
from torch_geometric_temporal.nn.recurrent import GCLSTM


class LSTMGCNModel(torch.nn.Module):
    def __init__(
            self,
            num_node_features,
            output_lstm,
            K,
            output_linear,
    ):
        """
        Graph convolutional model with embedded LSTM and relu transformation on outputs

        :param num_node_features: int
            The number of input features to the GCLSTM layer
        :param output_lstm: int
            The number of output features of the GCLSTM layer
        :param K: int
            The K-hop neighborhood for the current node
        :param output_linear: int
            The number of output features from the liear layer

        """

        super(LSTMGCNModel, self).__init__()
        self.lstm = GCLSTM(num_node_features, output_lstm, K)
        self.linear = torch.nn.Linear(output_lstm, output_linear)

    def forward(self, x, edge_index, edge_weight):
        """

        :param x: PyTorch Float Tensor
            Node features
        :param edge_index: PyTorch Float Tensor
            Graph edge indices
        :param edge_weight: PyTorch Float Tensor
            Edge weight vector

        :return:
            H: PyTorch Float Tensor
                Hidden state matrix for all nodes.
            C: PyTorch Float Tensor
                Cell state matrix for all nodes.

        """

        h, _ = self.lstm(x, edge_index, edge_weight)
        h = F.relu(h)
        h = self.linear(h)
        return h