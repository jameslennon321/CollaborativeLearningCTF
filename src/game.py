from model import *


class GameListener(object):

	def handle_loop(self, game_state):
		pass


class Game(object):

	def __init__(self, width=100, height=100, state_resolution=100):
		self.width            = width
		self.height           = height
		self.state_resolution = state_resolution

		self.transition_model = TransitionModel()
		self.reward_model     = RewardModel()

		self.agents      = [[],[]]
		self.team_agents = [None, None]
		self.listeners   = []
		self.game_state  = GameState(width, height, self)

	def add_agent(self, agent, pos, team):

		# check valid team
		if team not in (0,1):
			print "ERROR: Invalid team {}; must be 0 or 1.".format(team)
			return

		self.agents[team].append(agent)

		state      = State(self, len(self.game_state.states[team]) - 1)
		state.pos  = pos
		state.team = team
		self.game_state.states[team].append(state)

	def set_team_agent(self, team_agent, team):
		self.team_agents[team] = team_agent

	def add_listener(self, listener):
		self.listeners.append(listener)

	def run_team(self, team):

		if self.team_agents[team] is None:
			self.game_state.states[team] = \
				map(lambda a:
					self.run_agent(self.agents[team][a], self.game_state.states[team][a]),
					xrange(len(self.agents[team])))
		else:
			actions = self.team_agents[team].choose_actions(self.game_state, team)

			self.game_state.states[team] = \
				map(lambda a:
					self.run_agent(self.agents[team][a], self.game_state.states[team][a], actions[a]),
					xrange(len(self.agents[team])))


	def start(self):
		for j in (0,1):
			for i in xrange(len(self.game_state.states[j])):
				old_state = self.game_state.states[j][i]
				self.game_state.states[j][i] = \
					self.transition_model.apply_action(old_state, Action.stay, self.game_state) 

	def loop(self):
		# update game state
		self.run_team(0)
		self.run_team(1)

		# notify listeners
		map(lambda l: l.handle_loop(self.game_state), self.listeners)

	def run_agent(self, agent, state, action=None):
		if action is None:
			action    = agent.choose_action(state, self.game_state)

		new_state = self.transition_model.apply_action(state, action, self.game_state)
		reward    = self.reward_model.get_reward(state, action, new_state, self.game_state)

		agent.observe_transition(state, action, reward, new_state)

		return new_state






