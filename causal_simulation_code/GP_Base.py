
import numpy as np

from scipy.special import expit

import sklearn.gaussian_process as gp
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.utils import check_random_state

class GP_Base:
	def __init__(self, D=1, C_count=2, random_state=0, **kwargs):
		self.GP = GPR(**kwargs)
		self.D=D
		self.C_count=C_count
		self.random_state=random_state

	def sample(self, n=1000, kernels=[RBF(), RBF(length_scale=.8)], include_ground_truth=True):
		"""
			Parameters
			----------
			n : int
				Amount of data to sample.
			kernels : [Kernel]
				For every cause, there should be exactly one Kernel such that
				every cause corresponds with a different function. As such, 
				len(kernels) should equal C_count.
			include_ground_truth : Bool
				Indicates whether a response should be sampled for all treatments
				given a datapoint. Of course, this is not possible in real
				datasets.
			
			Returns
			-------
			A dataset of shape (n, D + 2) where the first D columns
			contain features, the penultimate column the applied treatment and
			the last column the response. If include_ground_truth is True, 
			the last two columns will be replaced with C_count columns indicating
			response to all treatments.
		"""
		X = np.random.rand(n, self.D)
		y = np.ndarray((n, self.C_count))

		for t in range(self.C_count):
			y_mean = self.GP.predict(X) 	# Thus far, the GP is untrained 
											# -> without a bias the mean should just be 0
											# the reason for using .predict is for future 
											# purpose

			rng = check_random_state(self.random_state)
			p = rng.multivariate_normal(y_mean, kernels[t](X), 1).T
			y.T[t] = np.array(list(map(lambda p: np.random.binomial(1, expit(p)), p))).T

		if not include_ground_truth:
			y = np.array(list(map(self.reduce_causes, y)))			

		data = np.append(X, y, axis=1)
		return data

	
	def reduce_causes(self, y):
		c = np.random.randint(self.C_count)
		return np.array([c, y[c]])

		


