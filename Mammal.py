import numpy as np
import matplotlib.pyplot as plt
from Simulation import *
from Signal import *
from dprint import dprint


class Mammal:

    def __init__(self, simulation, position, avg_speed=1):
        self.simulation = simulation
        direction = np.random.random() * 2 * np.pi
        self.state = np.array([position[0],
                               position[1],
                               np.cos(direction) * avg_speed,
                               np.cos(direction) * avg_speed,
                               direction])
        self.past_state = self.state
        self.avg_speed = avg_speed
        self.maxTurnAngle = 0.56
        self.sound_intensity = 100

    def dynamique(self):
        """
        :return: Derivative of state vector
        """
        direction_deriv = self.maxTurnAngle * np.random.standard_normal()
        x_accel = -direction_deriv * np.sin(self.state[-1]) * self.avg_speed
        y_accel = direction_deriv * np.cos(self.state[-1]) * self.avg_speed
        state_deriv = np.array([self.state[2], self.state[3], x_accel, y_accel, direction_deriv])
        return state_deriv

    def make_sound(self):
        """
            Generate a sound signal
        """
        self.simulation.signals.append(Signal(self.state[0:2], self.sound_intensity))

    def distance_to(self, thing):
        """
        :param thing: Object we want the distance to
        :return: Distance to thing
        """
        d = np.sqrt((self.state[0]-thing.state[0])**2 + (self.state[1]-thing.state[1])**2)
        return d

class Group(Mammal):

    def __init__(self, simulation, position):
        super().__init__(simulation, position)
        self.group_behavior = True
        self.detection_range = 10
        self.neighbors = []

    def dynamique(self):
        """

        :return: Derivative of state vector
        """
        direction_deriv = 0
        self.update_neighbors()
        if len(self.neighbors) != 0:
            center_of_group = self.find_center_of_group()
            group_direction = self.find_group_direction()

    def find_center_of_group(self):
        """
            Return the center coordinates of the group
        """
        t = []
        for i in range(len(self.neighbors)):
            t.append(self.neighbors[i].state[0:2])
        positions = np.array(t)
        x_center = np.mean(positions[:, 0])
        y_center = np.mean(positions[:, 1])
        return np.array([x_center, y_center])

    def find_group_direction(self):
        """
            Return the average direction of the group
        """
        directions = np.zeros(len(self.neighbors))
        for i in range(len(self.neighbors)):
            directions[i] = self.neighbors[i].state[-1]
        return np.mean(directions)

    def update_neighbors(self):
        """
            Updates the neighbors list of a mammal
        """
        self.neighbors = []
        mammals = self.simulation.mammals
        for i in range(len(mammals)):
            if self.distance_to(mammals[i]) < self.detection_range and mammals[i] is not self:
                self.neighbors.append(mammals[i])


if __name__ == "__main__":
    S = Simulation("txt", 3)
    S.populate()
    M1 = S.mammals[0]
    M1.update_neighbors()
    print(M1.find_center_of_group())
