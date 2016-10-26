from faker.generator import random
from faker.providers import BaseProvider

import random


class IntegerRangeProvider(BaseProvider):
    def range(self, start, stop):
        return random.randint(start, stop)

