import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from neuron_network import NeuronNetwork  # noqa: E402

DELTA = 0.15


@pytest.fixture(scope="module")
def network():
    return NeuronNetwork()


@pytest.mark.parametrize("triple", [
    (0.0, 0.0, 0.0),
    (1.0, 1.0, 1.0),
    (-1.0, -1.0, -1.0),
    (0.5, -0.2, 0.1),
    (-0.7, -0.3, -0.9),
    (0.2, 0.9, -0.4),
    (-0.5, 0.0, 0.8),
    (-1.0, 1.0, 0.0),
])
def test_finds_maximum_of_known_triples(network, triple):
    assert abs(network.max(*triple) - max(triple)) < DELTA


def test_output_stays_in_range(network):
    for triple in ([1.0, 1.0, 1.0], [-1.0, -1.0, -1.0], [0.3, -0.8, 0.6]):
        assert -1.0 <= network.predict(triple)[0] <= 1.0


def test_error_on_new_test_data_is_small(network):
    inputs, outputs = network.generate_data(1000)
    assert network.mean_absolute_error(inputs, outputs) < 0.05
