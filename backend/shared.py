
import json
from dataclasses import dataclass

@dataclass
class NetworkConfig:
    id: str
    input: list[str]
    expected_output: list[str]
    hidden_neuron_layer_size: int
    hidden_neuron_layers: int
    iterations_before_result: int

@dataclass
class NetworkResult:
    iterations: int
    last_input: list[int]
    last_expected_output: list[int]
    last_output: list[int]

@dataclass
class NetworkList:
    networks: list[dict]
