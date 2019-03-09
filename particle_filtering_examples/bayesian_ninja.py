# Particle Filtering example adapted from:
# http://studentdavestutorials.weebly.com/particle-filter-with-matlab-code.html
#
# An introduction to the problem is here: https://www.youtube.com/watch?v=O-lAJVra1PU
# The model is described in this YouTube video: https://www.youtube.com/watch?v=5dE4eCzT0CM
# A run-through of the Matlab code is here: https://www.youtube.com/watch?v=HZvF8KlFoWk
#
# Ninjas use a particle filter to try to chase the quail.
# Quail have a non-linear flight model (with imprecise measurements).
# 1-D model, discrete time steps.

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def update_position(x, t, sigma_squared_N):
    """
    Update the position of the quail.

    The quail's new position is given by:

    x = 0.5*x + 25*x/(1 + x^2) + 8*cos(1.2*(t-1)) + PROCESS NOISE

    where PROCESS NOISE ~ N(0, sqrt(sigma_squared_N)), i.e. it is normally distributed
    with a mean of zero and a standard deviation of sqrt(sigma_squared_N).

    :param x: Previous position of the quail.
    :param t: Current time index.
    :param sigma_squared_N: Variance of the process noise.
    :return: New position of the quail.
    """

    # Preconditions
    assert type(t) == int
    assert t >= 0
    assert type(sigma_squared_N) == float
    assert sigma_squared_N >= 0.0

    # Generate a sample of the process noise
    if len(x.shape) == 0:
        n = stats.norm.rvs(0, np.sqrt(sigma_squared_N))
    else:
        n = stats.norm.rvs(0, np.sqrt(sigma_squared_N), size=x.shape[0])

    # Return the new position of the quail
    return 0.5 * x + 25 * x / (1 + np.power(x, 2)) + 8 * np.cos(1.2 * (t - 1)) + n


def measurement(x, sigma_squared_R):
    """
    Measurement update function.

    The measurement is given by:

    z = x^2/20 + MEASUREMENT NOISE

    where MEASUREMENT NOISE ~ N(0, sqrt(x.R)).

    :param x: Position.
    :param sigma_squared_R: Variance of the measurement noise.
    :return: New measurement of the quail's position.
    """

    # Preconditions
    assert type(sigma_squared_R) == float
    assert sigma_squared_R >= 0

    # Generate a sample of the measurement noise
    n = stats.norm.rvs(0, np.sqrt(sigma_squared_R), size=x.shape)

    # Return the updated measurement
    return np.power(x, 2) / 20 + n


def probability_of_observation(z_hat, z, sigma_squared_R):
    """
    Calculate the probability of the observed position.

    :param z_hat: Predicted position.
    :param z: Observed position.
    :param sigma_squared_R: Variance of the measurement noise.
    :return: Probability of the predicted position.
    """

    # Return the probability of the observation
    return stats.norm.pdf(z_hat, z, sigma_squared_R)


def resample(x, p):
    """
    Perform re-sampling.

    :param x: Position of the particles.
    :param p: Probability of each of the particles.
    :return: Resampled vector.
    """

    # Preconditions
    assert x.shape == p.shape

    # Initialise the output array
    output = np.zeros(x.shape)

    # Determine the number of times each particle should be used
    n = x.shape[0]  # number of elements in the vector
    s = stats.multinomial.rvs(n, p)

    # Walk through each particle
    idx = 0
    for i in range(n):
        for j in range(s[i]):
            output[idx] = x[i]
            idx += 1

    # Postcondition
    assert x.shape == output.shape

    # Return the resampled vector
    return output


if __name__ == '__main__':

    # Initialise the variables
    x_initial = 0.1        # initial state (position) of the quail
    sigma_squared_N = 1.0  # noise variance for the state update
    sigma_squared_R = 1.0  # noise variance for the measurement
    t_max = 40             # duration (number of iterations of the chase)
    N = 100                # number of particles the system generates
    V = 2                  # variance of the initial estimate of each particle

    # Vector to hold the ground-truth position (state) of the quail
    x = np.zeros(t_max)
    x[0] = x_initial

    # Vector to hold the observations
    z = np.zeros((t_max, 1))
    z[0] = measurement(x[0], sigma_squared_R)

    # (N x t) matrix to hold the position of the particles
    x_particles = np.zeros((N, t_max))

    # (N x t) matrix to hold the observations of the particles
    z_particles = np.zeros((N, t_max))

    # Initialise the position of the particles
    # The prior distribution is modelled as a Normal distribution centred around the true value
    x_particles[:, 0] = stats.norm.rvs(x_initial, np.sqrt(V), size=N)

    # Initialise the measurements of the particles
    z_particles[:, 0] = measurement(x_particles[:, 0], sigma_squared_R)

    # Initialise the matrix to hold the probability of each particle
    p_particles = np.zeros((N, t_max))

    # Vector to hold the estimated position of the quail
    x_est = np.zeros(t_max)
    x_est[0] = np.mean(x_particles[:, 0], axis=0)

    # Walk through each time step
    for t in range(1, t_max):

        # Update the ground-truth position of the quail
        x[t] = update_position(x[t-1], t, sigma_squared_N)

        # Update the measurement of the quail (based on the ground-truth, but noisy)
        z[t] = measurement(x[t], sigma_squared_R)

        # Update the state of the particles
        x_particles[:, t] = update_position(x_particles[:, (t-1)], t, sigma_squared_N)

        # Update the observations of the particles
        # Note that noise is not applied because that happens during the actual
        # measurement process
        z_particles[:, t] = measurement(x_particles[:, t], 0.0)

        # Calculate the weights for the particles
        # The weights are based upon the probability of the observation for a
        # particle given the actual observation
        p_particles[:, t] = probability_of_observation(z_particles[:, t], z[t], sigma_squared_R)

        # Normalise the probabilities such that the distribution sums to 1
        total = np.sum(p_particles[:, t], axis=0)
        p_particles[:, t] = p_particles[:, t] / total

        # Perform re-sampling
        x_particles[:, t] = resample(x_particles[:, t], p_particles[:, t])

        # Get the final estimate using the (resampled) particles
        x_est[t] = np.mean(x_particles[:, t], axis=0)

    # Calculate the overall mean squared error
    mse = np.sum(np.power(x_est - x, 2)) / x.shape[0]
    print("Mean squared error = %f" % mse)

    # Generate a plot
    t_range = list(range(0, t_max))
    for t in range(t_max):
        plt.plot(np.repeat(t, N), x_particles[:, t], 'b.', alpha=0.2)

    plt.title("Position of the quail as a function of time")
    plt.plot(t_range, x, '--go', label="actual")
    plt.plot(t_range, x_est, 'b:x', label="estimated")
    plt.xlabel("Time index")
    plt.ylabel("Position")
    plt.legend()
    plt.show()
