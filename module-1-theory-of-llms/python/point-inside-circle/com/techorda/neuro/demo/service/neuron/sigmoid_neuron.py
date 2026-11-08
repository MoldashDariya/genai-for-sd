import math

from neuron.neuron import Neuron


class SigmoidNeuron(Neuron):
    """Neuron with the sigmoid activation function. Output range: (0, 1), read as a probability."""

    def __init__(self, input_count: int) -> None:
        super().__init__(input_count)

    def activation_function(self, x: float) -> float:
        # Two branches avoid math.exp overflow for large |x|.
        if x >= 0:
            return 1.0 / (1.0 + math.exp(-x))
        e = math.exp(x)
        return e / (1.0 + e)

    def derivative(self, x: float) -> float:
        """Derivative of sigmoid at the weighted sum x: f'(x) = f(x) * (1 - f(x))."""
        fx = self.activation_function(x)
        return fx * (1.0 - fx)
