import snakeGame
import NeuralNetwork
import random
import pickle

class Timeline:


    def Timeline(self):
        self.bestEvo = []
        self.bestGeneration = []

    def setBestEvo(self, fitness, nn):
        list = []
        list.append(fitness)
        list.append(nn)
        self.bestEvo = list

    def setBestGeneration(self, nnList):
        self.bestGeneration = nnList

    def NewEvolution(self, generations, species):
        nn = []
        for i in range(species):
            nn.append(NeuralNetwork.NeuralNet(16, 2, 8, 4))
        generation_results = snakeGame.gameLoop(nn, 1)

        for x in range(generations-1):

            # Calculate the total fitness scores, so we can randomize parent choices
            totalScores = generation_results[0][0]
            for i in range(len(generation_results) - 1):
                totalScores += generation_results[i+1][0]
                generation_results[i+1][0] += generation_results[i][0]

            # CHOOSING PARENTS AND MAKING OFFSPRING

            new_generation = []
            for y in range(species):

                parent1fitness = random.uniform(0, totalScores)
                # Calculate parent 1
                for i in range(len(generation_results)):
                    if parent1fitness < generation_results[i][0]:
                        parent1 = generation_results[i][1]
                        if i == 0:
                            p1Index = [0, generation_results[i][0]]
                        else:
                            p1Index = [generation_results[i-1][0], generation_results[i][0]]
                        break

                # If parent 2 randomization is the same, we must choose another because you should not be mating with yourself
                parent2fitness = random.uniform(0, totalScores)
                while parent2fitness > p1Index[0] and parent2fitness < p1Index[1]:
                    parent2fitness = random.uniform(0,totalScores)

                # Calculate parent 2
                for i in range(len(generation_results)):
                    if parent2fitness < generation_results[i][0]:
                        parent2 = generation_results[i][1]
                        break

                # Birth of new offspring

                new_generation.append(NeuralNetwork.NeuralNet(16, 2, 8, 4).offspring(parent1, parent2))

            with open("Timeline1.pkl", "wb") as pickle_file:
                pickle.dump(new_generation, pickle_file)
            generation_results = snakeGame.gameLoop(new_generation, x + 2)


    def playback(self, filename):
        with open(filename+".pkl", "rb") as pickle_file:
            data = pickle.load(pickle_file)
        snakeGame.gameLoop(data, "Replay")


a = Timeline()
a.NewEvolution(25, 50)

#a.playback("TimelineLOOP")