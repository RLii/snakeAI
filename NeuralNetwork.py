import numpy as np
import random


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class OutputNode:

    def __init__(self, in_weight, output, bias):
        self.in_weight = in_weight
        self.output = output
        self.bias = bias
        self.activation = 0

    def set_activation(self,activation):
        self.activation = activation

    def get_activation(self):
        return self.activation

class InputNode:

    def __init__(self, inputs, out_weights, bias):
        self.inputs = inputs
        self.out_weights = out_weights
        self.bias = bias

    def get_weight(self, x):
        return self.out_weights[x]

    def set_inputs(self, x):
        self.inputs = x

    def get_inputs(self):
        return self.inputs


class HiddenNode:

    def __init__(self, bias, in_weights, out_weights):
        self.in_weights = in_weights
        self.out_weights = out_weights
        self.bias = bias
        self.activation = 0

    def get_out_weight(self, x):
        return self.out_weights[x]

    def set_activation(self, activation):
        self.activation = activation

    def get_activation(self):
        return self.activation


class NeuralNet:

    def __init__(self, num_of_inputs, num_of_hidden_layers, num_of_hidden_nodes, num_of_outputs):
        # VARIABLES
        weight_initialization = 3

        # INITIALIZE INPUT NODES
        self.input_nodes = []
        for i in range(num_of_inputs):
            weights = []
            for x in range(num_of_hidden_nodes):
                weights.append(random.uniform(-weight_initialization, weight_initialization))

            # INPUTS ARE A NULL LIST ATM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            inputs = []
            self.input_nodes.append(InputNode(inputs, weights, 0))

        # INITIALIZE HIDDEN NODES
        self.hidden_layers = []
        for i in range(num_of_hidden_layers):
            hidden_nodes = []
            # BUILDING WEIGHTS FOR EACH NODE
            for x in range(num_of_hidden_nodes):
                weights_out = []
                weights_in = []
                if i == num_of_hidden_layers - 1:
                    for y in range(num_of_outputs):
                        weights_out.append(random.uniform(-weight_initialization, weight_initialization))
                else:
                    for y in range(num_of_hidden_nodes):
                        weights_out.append(random.uniform(-weight_initialization, weight_initialization))
                if i == 0:
                    for y in self.input_nodes:
                        weights_in.append(y.get_weight(x))
                else:
                    for y in self.hidden_layers[i-1]:
                        weights_in.append(y.get_out_weight(x))
                hidden_nodes.append(HiddenNode(0, weights_in, weights_out))

            self.hidden_layers.append(hidden_nodes)

        # INITIALIZE OUTPUT NODES
        self.output_nodes = []
        for i in range(num_of_outputs):
            weights = []
            for x in range(num_of_hidden_nodes):
                weights.append(self.hidden_layers[num_of_hidden_layers-1][x].get_out_weight(i))
            # OUTPUT NOT INITIALIZED YET !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            output = []
            self.output_nodes.append(OutputNode(weights, output, 0))

    def forward_propagate(self, inputs):

        #CALCULATING THE ACTIVATION FOR THE FIRST HIDDEN LAYER

        input_matrix = []
        weight_matrix = []

        # Retrieving the input matrix for the input
        for i in range(len(self.input_nodes)):
            self.input_nodes[i].set_inputs(inputs[i])
            input_matrix.append(self.input_nodes[i].get_inputs())

        input_matrix = np.array(input_matrix).reshape(1, 24)

        # Retrieving the weight matrix for the input to hidden layer
        input_to_hidden_weights = []
        for x in range(len(self.input_nodes)):
            for y in range(len(self.hidden_layers[0])):
                input_to_hidden_weights.append(self.input_nodes[y].get_weight(x))
            weight_matrix.append(input_to_hidden_weights)











a = NeuralNet(24, 2, 16, 4)
a.forward_propagate([2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7])
