# Causal Simulations for Uplift Modeling
This is an accompanying repository for a paper, submitted to the AAAI Spring Symposium on [_Beyond Curve Fitting: Causation, Counterfactuals, and Imagination-based AI_](https://why19.causalai.net). In it you will find code and documentation, representing the ideas discussed in the paper, as well as extra (animated) visualisations. 

The paper focusses on a number of requirements that must be defined for any causal simulation. These requirements will form a guideline throughout the documentation of this code.

### Base functions
A core idea behind the discussed papers is one of _base functions_. Two base functions are present in the current code base:
#### `Sine_Base(D, f, G)`
`D` is the dimension count, `f` is the frequency and `G` (displacement vector) will govern the average causal effect in the simulation. 
#### `Polynomial_Base(D, q, K)`
Here, `K` (the coefficient vector) implies a crucial difference with the `Sine_Base` as it implies that a `Polynomial_Base` must be created for every cause. This choice is motivated by the fact that one can control the difference between two `coefficient_vector`'s while in a `Sine_Base`, this difference is already controlled by the `displacement_vector`.

### Drift
Drift is controlled by the top level class `Simulation(C, D, base_functions, drift_rate, drift_over_time, sudden_drift, drift_moments, std)` through its parameters `drift_rate`, `drift_over_time`, `sudden_drift` and `drift_moments` where the first three are necessary when random drift is required. These first three parameters can be omitted when the `drift_moments` are chosen before the simulation is running. These moments are moments in function of a `t` representing an experiment number. When the drift moments are to be chosen randomly by the `Simulation`, `drift_rate` describes the _amount_ that is drifted, `drift_over_time` governs how often or how gradual the drift is taking place and `sudden_drift` is `False` when the `drift_rate` is linearly distributed over `drift_over_time` and `True` when (on average) the complete `drift_rate` happens once in `drift_over_time`.

Drift for the `Sine_Base` is illustrated below.

![Alt Text](https://media.giphy.com/media/37QNktv30GTzdGnPgA/giphy.gif)

### Effect
When every a cause `C` is chosen, one can call `.chose_cause(C)` and an effect is returned. When a response is required that does not include drift or noise the method can be called as `.chose_cause(C, drift=False, n=False)`.

### Evaluation
In case of uplift modeling, one can consult the actual (ground truth) uplift for a specific `x` by calling `.get_sim_uplift(x)` on a `Simulation`. Other intricacies of the simulation can be acquired upon extension.

### Noise
As an extra parameter to `Simulation`, `std` governs the standard deviation of the Gaussian noise over the returned effect of the simulation. Extensions towards other distributions for noise must be added manually.