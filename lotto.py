from util import *

from ticket import Ticket


class Lotto:
    win_table = {
        "7": 2000000,
        "6+1": 100000,
        "6": 2000,
        "5": 50,
        "4": 10,
        "3+1": 2
    }

    def __init__(self):
        self.winning_numbers, self.bonus = Util().generate_numbers(bonus=True)

    def results(self, numbers):
        results = []
        rows = []

        for row in numbers:
            same_numbers = np.intersect1d(self.winning_numbers[0], row)
            bonus_hit = bool(np.intersect1d(self.bonus, row))
            hits = len(same_numbers)
            result_string = f"{hits}+{int(bonus_hit)}"
            if hits > 3 or (hits == 3 and bonus_hit == "True"):
                rows.append(sorted(row[0]))
            results.append([hits, bonus_hit, result_string])

        return np.array(results), rows

    def calculate_winnings(self, results):
        winnings = 0
        winning_rows = []
        number_of_wins = 0

        for result in results:
            number_of_hits = result[0]
            bonus_hit = result[1]
            res_string = result[2]

            if (number_of_hits == "3" or number_of_hits == "6") and bonus_hit == "True":
                win = self.win_table.get(res_string)
            else:
                win = self.win_table.get(number_of_hits)
            if win is not None:
                winning_rows.append(result)
                number_of_wins += 1
                winnings += win

        return winnings, number_of_wins, np.array(winning_rows)

    def generate_ticket(self):
        generated_tickets = 0

        while True:
            generated_tickets += 1
            ticket = Ticket(rows=1)
            lotto = Lotto()

            player_numbers = ticket.numbers
            results = lotto.results(player_numbers)
            ticket.money_won, ticket.winning_rows, ticket.winning_rows = lotto.calculate_winnings(results)
            ticket.unique_wins = Util().unique_wins(ticket.winning_rows)

            if ticket.money_won > 0 or generated_tickets > 1000:
                break

        print(f"Generated tickets: {generated_tickets}")
        print(ticket)

    def get_winning_row(self):
        return sorted(self.winning_numbers[0][0]), self.bonus
