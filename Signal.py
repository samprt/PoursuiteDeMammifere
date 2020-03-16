class Signal:

    def __init__(self, source, intensity):
        self.__source = source
        self.__source_intensity = intensity
        self.radius = 0.

    def dynamique(self):
        radius_deriv = 1500.
        return radius_deriv

