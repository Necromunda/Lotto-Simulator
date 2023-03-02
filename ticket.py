from util import *


class Ticket:
    def __init__(self, rows=1):
        self.rows = rows
        self.numbers = Util().generate_numbers(rows=self.rows)
        self.money_won = 0
        self.winning_rows = []
        self.initial_ticket_value = rows * 1
        self.unique_wins = {}

        plus_number = False

    def __str__(self):
        return f"Unique wins: {self.unique_wins}\n" \
               f"Rows bought: {self.rows}\n" \
               f"Number of winning rows: {len(self.winning_rows)}\n" \
               f"Money spent: {self.initial_ticket_value}\n" \
               f"Money won: {self.money_won}\n" \
               f"ROI: {round((self.money_won - self.initial_ticket_value) / self.initial_ticket_value * 100, 2)} %"