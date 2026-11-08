from neuron.neuron import Neuron


class ReluNeuron(Neuron):
    """
    Neuron with the ReLU activation function: f(x) = max(0, x).
    ReLU networks represent piecewise linear functions (such as max) very well:
    max(a, b) = b + relu(a - b).
    """

    def __init__(self, input_count: int) -> None:
        super().__init__(input_count)

    def activation_function(self, x: float) -> float:
        return x if x > 0.0 else 0.0

    def derivative(self, x: float) -> float:
        """Derivative of ReLU at the weighted sum x: 1 if x > 0, otherwise 0."""
        return 1.0 if x > 0.0 else 0.0
