import customtkinter
import tkinter as tk
import time

from lotto import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

win_table = {
    "7": 2000000,
    "6+1": 100000,
    "6": 2000,
    "5": 50,
    "4": 10,
    "3+1": 2
}


class Menu(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.change_scaling_event = None
        self.change_appearance_mode_event = None
        self.sidebar_button_event = None

        self.scale = 1
        self.value = 500
        self.numbers = ""
        self.bonus_number = ""

        # self.app = customtkinter.CTk()

        self.title("Lotto simulator")
        self.geometry(f"{1200}x{600}")
        self.resizable(False, False)

        # Configure 4x4 grid
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Games", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Lotto", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # Winning lotto numbers grid
        self.lotto_number_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.lotto_number_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=(10, 0), pady=10)

        self.winning_row_label = customtkinter.CTkLabel(self.lotto_number_frame, text="Winning row:", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.winning_row_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.winning_bonus_number_label = customtkinter.CTkLabel(self.lotto_number_frame, text="Bonus number:", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.winning_bonus_number_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.lotto_number_label = customtkinter.CTkLabel(self.lotto_number_frame, text=self.numbers, font=customtkinter.CTkFont(size=28, weight="bold"))
        self.lotto_number_label.grid(row=0, column=2, columnspan=10, sticky="w")

        self.bonus_number_label = customtkinter.CTkLabel(self.lotto_number_frame, text=self.bonus_number, font=customtkinter.CTkFont(size=28, weight="bold"))
        self.bonus_number_label.grid(row=1, column=2, columnspan=10, sticky="w")

        # Win chart
        self.win_chart_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.win_chart_frame.grid(row=0, column=3, rowspan=2, sticky="new", padx=10, pady=10)

        i = 0
        for key, value in win_table.items():
            _ = customtkinter.CTkLabel(self.win_chart_frame, text=f"{key}", font=customtkinter.CTkFont(size=20, weight="bold"))
            _.grid(row=i, column=3, sticky="w", pady=2, padx=10)
            _ = customtkinter.CTkLabel(self.win_chart_frame, text=f"{value} €", font=customtkinter.CTkFont(size=20, weight="bold"))
            _.grid(row=i, column=4, sticky="e", pady=2, padx=10)
            i += 1

        # Result grid
        self.result_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.result_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=(10, 0), pady=(0, 10))
        self.result_frame.grid_rowconfigure(0, weight=1)

        self.rows_played_label = customtkinter.CTkLabel(self.result_frame, text="Stats", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.rows_played_label.grid(row=0, column=1, sticky="new", pady=2, padx=10)

        self.rows_played_label = customtkinter.CTkLabel(self.result_frame, text="Rows played:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.rows_played_label.grid(row=1, column=0, sticky="w", pady=2, padx=10)

        self.rows_played_value_label = customtkinter.CTkLabel(self.result_frame, text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.rows_played_value_label.grid(row=1, column=1, sticky="w", pady=2, padx=10)

        self.winning_rows_label = customtkinter.CTkLabel(self.result_frame, text="Winning rows:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.winning_rows_label.grid(row=2, column=0, sticky="w", pady=2, padx=10)

        self.winning_rows_value_label = customtkinter.CTkLabel(self.result_frame, text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.winning_rows_value_label.grid(row=2, column=1, sticky="w", pady=2, padx=10)

        self.money_won_label = customtkinter.CTkLabel(self.result_frame, text="Money won:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.money_won_label.grid(row=3, column=0, sticky="w", pady=2, padx=10)

        self.money_won_value_label = customtkinter.CTkLabel(self.result_frame, text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.money_won_value_label.grid(row=3, column=1, sticky="w", pady=2, padx=10)

        self.roi_label = customtkinter.CTkLabel(self.result_frame, text="ROI:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.roi_label.grid(row=4, column=0, sticky="w", pady=2, padx=10)

        self.roi_value_label = customtkinter.CTkLabel(self.result_frame, text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.roi_value_label.grid(row=4, column=1, sticky="w", pady=2, padx=10)

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Winning rows", corner_radius=10)
        self.scrollable_frame.grid(row=3, column=1, sticky="sew", padx=(10, 0))
        # self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Create ticket frame
        self.result_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.result_frame.grid(row=1, column=2, rowspan=3, sticky="nsew", padx=(10, 0), pady=(0, 10))

        # Create ticket slider and simulate button
        self.slider_scale_label = customtkinter.CTkLabel(self, text="Slider scale x1000")
        self.slider_scale_label.grid(row=2, column=3, sticky="sew")

        self.slider_scale = customtkinter.CTkOptionMenu(self, values=["1", "10", "100", "1000"], command=self.slider_scale_callback)
        self.slider_scale.grid(row=3, column=3, padx=10, pady=(20, 20), sticky="sew")

        self.simulate_button = customtkinter.CTkButton(master=self, text="Simulate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.simulate)
        self.simulate_button.grid(row=4, column=3, padx=10, pady=(20, 20), sticky="nsew")

        self.ticket_label = customtkinter.CTkLabel(self, text=f"Tickets: {self.value}")
        self.ticket_label.grid(row=3, column=1, columnspan=2, sticky="sew")

        self.slider = customtkinter.CTkSlider(self, from_=1, to=1000, command=self.slider_callback, button_color="blue", hover=False)
        self.slider.set(self.value)
        self.slider.grid(row=4, column=1, columnspan=2, pady=(20, 20), sticky="nsew")

    def simulate(self):
        start_time = time.time()

        util = Util()
        ticket = Ticket(rows=self.value)
        lotto = Lotto()

        player_numbers = ticket.numbers
        results, rows = lotto.results(player_numbers)
        ticket.money_won, ticket.winning_rows, ticket.winning_rows = lotto.calculate_winnings(results)
        ticket.unique_wins = util.unique_wins(ticket.winning_rows)

        winning_row = lotto.get_winning_row()

        self.lotto_number_label.configure(text=winning_row[0])
        self.bonus_number_label.configure(text=winning_row[1])

        self.rows_played_value_label.configure(text=ticket.rows)
        self.winning_rows_value_label.configure(text=len(ticket.winning_rows))
        self.money_won_value_label.configure(text=f"{ticket.money_won} €" if ticket.money_won > 0 else "0")
        self.roi_value_label.configure(text=f"{round((ticket.money_won - ticket.initial_ticket_value) / ticket.initial_ticket_value * 100, 2)} %")
        # i = 0
        # for row in rows:
        #     _ = customtkinter.CTkLabel(self.scrollable_frame, text=f"{row}", font=customtkinter.CTkFont(size=20, weight="bold"))
        #     _.grid(row=i, column=0, sticky="w")
        #     i += 1

        print(ticket)

        exec_time = round(time.time() - start_time, 5)
        print(f"\nExecution time {exec_time} s")

    def slider_callback(self, value):
        self.value = int(value)
        self.ticket_label.configure(text=f"Tickets: {self.value}")
        # print(self.value)

    def slider_scale_callback(self, new_scale):
        slider_value = int(self.slider.get())
        upper_boundary = 1000 * int(new_scale)

        self.slider.configure(to=upper_boundary)

        scaled_value = int(slider_value * int(new_scale) / self.scale)
        self.slider.set(scaled_value)
        self.ticket_label.configure(text=f"Tickets: {scaled_value}")
        self.value = scaled_value
        self.scale = int(new_scale)

    def handle_progress(self):
        return
