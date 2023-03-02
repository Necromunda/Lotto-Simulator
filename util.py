import random
import numpy as np


class Util:
    def generate_numbers(self, rows=1, bonus=False):
        ticket = []

        for _ in range(rows):
            numbers = [random.sample(range(1, 41), 7)]
            # numbers.append(random.sample(range(1, 41), 7))

            numbers.sort()
            ticket.append(numbers)

            if bonus:
                bonus_number = random.randint(1, 40)
                return np.array(ticket, dtype=int), bonus_number

        return np.array(ticket, dtype=int)

    def unique_wins(self, rows):
        wins = {
            "7 oikein": 0,
            "6+1 oikein": 0,
            "6 oikein": 0,
            "5 oikein": 0,
            "4 oikein": 0,
            "3+1 oikein": 0
        }

        if len(rows) == 0:
            return {}

        for row in rows:
            # bonus_hit = not bool(row[1])

            if row[0] == "3":
                wins["3+1 oikein"] += 1
            elif row[0] == "4":
                wins["4 oikein"] += 1
            elif row[0] == "5":
                wins["5 oikein"] += 1
            elif row[0] == "6":
                if row[1] == "False":
                    wins["6 oikein"] += 1
                else:
                    wins["6+1 oikein"] += 1
            elif row[0] == "7":
                wins["7 oikein"] += 1

        return wins
