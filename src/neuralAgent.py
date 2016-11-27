from agent import *
from testAgents import *
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import TanhLayer, LinearLayer

class NeuralAgent(QLearningAgent):

	def setup_approximation(self, n):
		self.neural_net = buildNetwork(n, 6, 1, bias=True, hiddenclass=LinearLayer, outclass=LinearLayer)
		self.trainer    = BackpropTrainer(self.neural_net)

	def value_of_state(self, state_vector):
		return self.neural_net.activate(state_vector)[0]

	def learn_q(self, state_vector, action, old, new):
		ds = SupervisedDataSet(len(state_vector), 1)
		ds.addSample(state_vector, new)

		self.trainer.setData(ds)
		self.trainer.trainEpochs(10)
		