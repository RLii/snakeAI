import numpy
import random


def sigmoid(x):
    return 1 / (1 + numpy.exp(-x))


class OutputNode:

    def __init__(self, weights, output,bias):
        self.weights = weights
        self.output = output


class InputNode:

    def __init__(self, inputs, weights, bias):
        self.inputs = inputs
        self.weights = weights


class HiddenNode:

    def __init__(self, bias, inweights, outweights):
        self.inweights = inweights
        self.outweights = outweights
        self.bias = bias


class NeuralNet:

    def __init__(self, numofinput, numofhiddenlayers, numofhiddennodes, numofoutput):
        self.input_nodes = []
        for i in range(numofinput):
            weights = []
            bias = []
            for x in range(numofinput):
                bias.append(0)
            for x in range(numofhiddennodes):
                weights.append(random.uniform(-3, 3))
            # INPUTS ARE A NULL LIST ATM
            inputs = []
            self.input_nodes.append(InputNode(inputs, weights, bias))

        self.hidden_layers = []
        for i in range(numofhiddenlayers):
            hidden_nodes = []
            weights = []
            bias = []
            for x in range(numofhiddennodes):
                bias.append(0)
            for x in range(numofhiddennodes):
                if i == numofhiddenlayers - 1:
                    for y in range(numofoutput):
                        weights.append(random.uniform(-3, 3))
                else:
                    for y in range(numofhiddennodes):
                        weights.append(random.uniform(-3, 3))
            hidden_nodes.append(HiddenNode(bias, weights))
            self.hidden_layers.append(hidden_nodes)

        self.output_nodes = []
        for i in range(numofoutput):



NeuralNet(24, 2, 16, 4)
