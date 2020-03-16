from Mammal import *
# from Ecosystem import *
# from Signal import *
from dprint import dprint


class Simulation:

    def __init__(self, map_file="map.txt", nb_mammals=10, sim_time=100):
        self.deltatime = 0.01
        self.sim_time = sim_time
        self.clock = 0.
        # self.ecosystem = Ecosystem(map_file)
        self.mammals = np.zeros(nb_mammals, dtype=Mammal)
        self.signals = []
        self.sim_data = []

    def populate(self):
        """
            Fills the ecosystem with marine mammals
        """
        i = 0
        coords = []
        while i < len(self.mammals):
            x = np.random.randint(0, 10)
            y = np.random.randint(0, 10)
            if [x, y] not in coords:
                coords.append([x, y])
                i += 1
        for t in range(len(self.mammals)):
            self.mammals[t] = Group(self, np.array(coords[t]))

    def update(self):
        """
            Update simulation
        """
        for i in self.mammals:
            self.euler_mammal(i)
        for i in self.signals:
            self.euler_signal(i)
        self.clock += self.deltatime

    def run(self):
        """
            Run simulation
        """
        self.populate()

        updates_per_seconds = int(1/self.deltatime)
        delay_not_occured = True
        for i in range(self.sim_time):
            position = []
            # TODO: keep track of simulation status at certain time
            for k in self.mammals:
                position.append(k.state[0:2])
            self.sim_data.append(position)

            for t in range(updates_per_seconds):
                if self.clock != i + t*self.deltatime and delay_not_occured:
                    print("Delay occured at", self.clock, "seconds. Should be :", i + t*self.deltatime)
                    delay_not_occured = False

                self.update()

    def plot_simulation(self):
        A = np.array(self.sim_data)
        plt.plot(A[:, :, 0], A[:, :, 1])
        plt.show()

    def euler_mammal(self, mammal):
        mammal.state = mammal.state + mammal.dynamique()*self.deltatime

    def euler_signal(self, signal):
        signal.radius = signal.radius + signal.dynamique()*self.deltatime


if __name__ == "__main__":
    S = Simulation()
    S.run()
    S.plot_simulation()
