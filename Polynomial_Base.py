import numpy as np
import math

class Polynomial_Base:
	def __init__(self, D=2, n=5, K=np.ones(6)):
		self.D = D
		self.n = n
		self.U = self.u()

		if len(K) != self.n + 1:
			raise ValueError("Length of coefficient vector K does not match with maximum degree n!")
		
		self.K = K
	
	def u(self):
		out = np.empty((self.n + 1, self.D))
		for i in range(self.n + 1):
			out[i] = np.random.multinomial(i, np.ones(self.D)/self.D, size=1)[0]
		return out
	
	def h(self, d):
		return math.sin(d)
	
	def logistic(self, x):
		return (1 + np.exp(-x)) ** -1
	
	def eval(self, x, d, C):
		val = np.ones(self.n + 1)
		for i in range(self.n + 1):
			for j in range(self.D):
				val[i] *=  x[j] ** self.U[i][j]
		return self.logistic(np.dot(np.full(self.n + 1, self.h(d)) + self.K, val))