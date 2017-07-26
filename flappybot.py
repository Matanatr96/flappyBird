import json
import csv
class FlappyBirdBot(object):
	def __init__(self):
		self.iteration = 1389
		self.learn_rate = 0.28683100417866925
		self.reward = {0: 1, 1: -1000} #0 as dying, 1 as flapping
		self.load_qvalues()
		self.actions = []
		self.prev_state = "420,240,0"
		self.prev_action = 0
		self.scores = []


	def load_qvalues(self):
		#Sets the qvalues from the numpy file
		self.qvalues = {}
		with open("qmatrix.json") as qmatrix:
			self.qvalues = json.load(qmatrix)

	def run(self, pipeX, pipeY, velocity):
		# this method will automate the bot playing
		newState = self.map_state(pipeX, pipeY, velocity)
		# Action structure [s, a, s'] = prev_state, action, state
		self.actions.append((self.prev_state, self.prev_action, newState))
		self.prev_state = newState
		
		
		if self.qvalues[newState][0] >= self.qvalues[newState][1]:
			self.prev_action = 0
		else: 
			self.prev_action = 1

		return self.prev_action



	def save_qvalues(self):
		# Saves the Q-matrix as a JSON file every 10 iterations
		if self.iteration % 10 == 0:
			with open("qmatrix.json", "w") as qmatrix:
				json.dump(self.qvalues, qmatrix)
				print("QMatrix updated.")

	def map_state(self, pipeX, pipeY, velocity):
		if pipeX < 140:
			pipeX = int(pipeX) - (int(pipeX) % 10)
		else:
			pipeX = int(pipeX) - (int(pipeX) % 70)

		if pipeY < 180:
			pipeY = int(pipeY) - (int(pipeY) % 10)
		else:
			pipeY = int(pipeY) - (int(pipeY) % 60)

		return str(int(pipeX))+','+str(int(pipeY))+','+str(velocity)

	
	def prev_state(self):
		return self.prev_state


	def write_scores(self, score):
		score.append(self.learn_rate)
		with open(r'scores', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(score)


	def score_update(self, score):
		actionList = list(reversed(self.actions))
		upperPipeDeath = False 
		if len(actionList) > 0:
			if int(actionList[0][2].split(',')[1]) > 120:
				upperPipeDeath = True
			else:
				upperPipeDeath = False

		t = 1
		for move in actionList:
			state = move[0]
			act = move[1]
			res_state = move[2]
			if t == 1 or t==2:
				self.qvalues[state][act] = (1- self.learn_rate) * (self.qvalues[state][act]) + (self.learn_rate) * ( self.reward[1] + 1.0*max(self.qvalues[res_state]) )

			elif upperPipeDeath and act:
				self.qvalues[state][act] = (1- self.learn_rate) * (self.qvalues[state][act]) + (self.learn_rate) * ( self.reward[1] + 1.0*max(self.qvalues[res_state]) )
				upperPipeDeath = False

			else:
				self.qvalues[state][act] = (1- self.learn_rate) * (self.qvalues[state][act]) + (self.learn_rate) * ( self.reward[0] + 1.0*max(self.qvalues[res_state]) )
			t += 1

		self.write_scores([self.iteration, score])
		# n = float(self.iteration/1000)
		self.learn_rate = self.learn_rate*.9991
		self.iteration += 1 #updates number of iterations
		self.save_qvalues()
		self.actions = []

