import datetime
import numpy as np


class Model:
    def __init__(self, n: int) -> None:
        rng = np.random.default_rng(1337)
        self.entities = np.zeros(shape=(n, 4))
        self.entities[:, :2] = rng.uniform(-500.0, 500.0, size=(n, 2))
        self.entities[:, 2:] = rng.uniform(-10.0, 10.0, size=(n, 2))

    def update(self, dt: datetime.timedelta) -> None:
        self.entities[:, :2] += self.entities[:, 2:] * dt.total_seconds()
        self.entities[np.abs(self.entities[:, 0]) > 500, 2] *= -1
        self.entities[np.abs(self.entities[:, 1]) > 500, 3] *= -1

    def get(self) -> tuple[np.array, np.array]:
        return (self.entities[:, 0], self.entities[:, 1])
