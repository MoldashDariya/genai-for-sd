import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from neuron_network import NeuronNetwork  # noqa: E402


@pytest.fixture(scope="module")
def network():
    return NeuronNetwork()


@pytest.mark.parametrize("x, y", [(0, 0), (1, 1), (3, 3), (-2, 4), (0, -4.5), (4, -1)])
def test_points_inside_circle_return_one(network, x, y):
    assert network.classify(x, y) == 1


@pytest.mark.parametrize("x, y", [(6, 6), (0, -7), (-8, 2), (5.5, 0), (9, -9), (-4, 4)])
def test_points_outside_circle_return_zero(network, x, y):
    assert network.classify(x, y) == 0


def test_accuracy_on_new_test_data_is_high(network):
    inputs, outputs = network.generate_data(1000)
    assert network.accuracy(inputs, outputs) > 0.9
