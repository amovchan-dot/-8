import tkinter as tk
from tkinter import messagebox


class CurrencyExchangeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обмін валюти з гаманцем")
        self.root.geometry("450x470")
        self.root.resizable(False, False)


        self.wallet = {
            "UAH": 10000.00,
            "USD": 200.00,
            "EUR": 150.00
        }


        self.rates = {
            "USD": {"buy": 41.20, "sell": 41.75},
            "EUR": {"buy": 44.50, "sell": 45.20}
        }


        self.currency_var = tk.StringVar(value="USD")
        self.operation_var = tk.StringVar(value="buy")

        self._build_ui()
        self._update_wallet_display()
        self._update_default_rate()

    def _build_ui(self):

        wallet_frame = tk.LabelFrame(
            self.root, text="Ваш гаманець (поточний баланс)", padx=10, pady=8,
            font=("Arial", 9, "bold"), fg="#1c4587"
        )
        wallet_frame.pack(fill="x", padx=15, pady=(10, 6))

        self.lbl_uah = tk.Label(wallet_frame, font=("Arial", 10, "bold"))
        self.lbl_uah.pack(side="left", expand=True)

        self.lbl_usd = tk.Label(wallet_frame, font=("Arial", 10, "bold"))
        self.lbl_usd.pack(side="left", expand=True)

        self.lbl_eur = tk.Label(wallet_frame, font=("Arial", 10, "bold"))
        self.lbl_eur.pack(side="left", expand=True)


        curr_frame = tk.LabelFrame(self.root, text="1. Оберіть валюту (RadioButton)", padx=10, pady=8)
        curr_frame.pack(fill="x", padx=15, pady=6)

        tk.Radiobutton(
            curr_frame, text="Долар США (USD)", variable=self.currency_var,
            value="USD", command=self._update_default_rate
        ).pack(side="left", padx=20)

        tk.Radiobutton(
            curr_frame, text="Євро (EUR)", variable=self.currency_var,
            value="EUR", command=self._update_default_rate
        ).pack(side="left", padx=20)


        op_frame = tk.LabelFrame(self.root, text="2. Операція обмінного пункту (RadioButton)", padx=10, pady=8)
        op_frame.pack(fill="x", padx=15, pady=6)

        tk.Radiobutton(
            op_frame, text="Здати валюту (отримати грн у гаманець)", variable=self.operation_var,
            value="buy", command=self._update_default_rate
        ).pack(anchor="w", padx=10)

        tk.Radiobutton(
            op_frame, text="Купити валюту (оплатити грн з гаманця)", variable=self.operation_var,
            value="sell", command=self._update_default_rate
        ).pack(anchor="w", padx=10)


        edit_frame = tk.LabelFrame(self.root, text="3. Параметри розрахунку (Edit)", padx=10, pady=10)
        edit_frame.pack(fill="x", padx=15, pady=6)

        tk.Label(edit_frame, text="Поточний курс (грн):").grid(row=0, column=0, sticky="w", pady=4)
        self.edit_rate = tk.Entry(edit_frame, width=18, font=("Arial", 10))
        self.edit_rate.grid(row=0, column=1, padx=10, pady=4)

        self.lbl_amount = tk.Label(edit_frame, text="Сума валюти для здачі:")
        self.lbl_amount.grid(row=1, column=0, sticky="w", pady=4)
        self.edit_amount = tk.Entry(edit_frame, width=18, font=("Arial", 10))
        self.edit_amount.insert(0, "50")
        self.edit_amount.grid(row=1, column=1, padx=10, pady=4)

        tk.Label(edit_frame, text="Сума в гривнях:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="w", pady=4)
        self.edit_result = tk.Entry(edit_frame, width=18, font=("Arial", 10, "bold"), fg="#0b5394")
        self.edit_result.grid(row=2, column=1, padx=10, pady=4)


        btn_frame = tk.Frame(self.root, pady=12)
        btn_frame.pack(fill="x", padx=15)

        tk.Button(
            btn_frame, text="Обміняти", width=16, bg="#d9ead3", font=("Arial", 10, "bold"),
            command=self.calculate_and_exchange
        ).pack(side="left", padx=15)

        tk.Button(
            btn_frame, text="Вихід", width=16, bg="#f4cccc", font=("Arial", 10),
            command=self.root.quit
        ).pack(side="right", padx=15)

    def _update_wallet_display(self):

        self.lbl_uah.config(text=f"UAH: {self.wallet['UAH']:.2f} ₴")
        self.lbl_usd.config(text=f"USD: {self.wallet['USD']:.2f} $")
        self.lbl_eur.config(text=f"EUR: {self.wallet['EUR']:.2f} €")

    def _update_default_rate(self):

        curr = self.currency_var.get()
        op = self.operation_var.get()
        rate = self.rates[curr][op]

        self.edit_rate.delete(0, tk.END)
        self.edit_rate.insert(0, f"{rate:.2f}")

        if op == "buy":
            self.lbl_amount.config(text=f"Сума {curr} для здачі:")
        else:
            self.lbl_amount.config(text=f"Сума {curr} для купівлі:")

        self.edit_result.delete(0, tk.END)

    def calculate_and_exchange(self):

        try:
            rate = float(self.edit_rate.get().replace(",", "."))
            amount = float(self.edit_amount.get().replace(",", "."))

            if rate <= 0 or amount <= 0:
                raise ValueError("Курс та сума мають бути більшими за нуль.")

            curr = self.currency_var.get()
            op = self.operation_var.get()
            total_uah = round(amount * rate, 2)

            if op == "buy":

                if self.wallet[curr] < amount:
                    messagebox.showwarning(
                        "Недостатньо коштів",
                        f"У вашому гаманці лише {self.wallet[curr]:.2f} {curr}, а потрібно {amount:.2f} {curr}."
                    )
                    return

                self.wallet[curr] -= amount
                self.wallet["UAH"] += total_uah
                result_text = f"+{total_uah:.2f} грн"
            else:

                if self.wallet["UAH"] < total_uah:
                    messagebox.showwarning(
                        "Недостатньо коштів",
                        f"У вашому гаманці лише {self.wallet['UAH']:.2f} грн, а потрібно {total_uah:.2f} грн."
                    )
                    return

                self.wallet["UAH"] -= total_uah
                self.wallet[curr] += amount
                result_text = f"-{total_uah:.2f} грн"

            self.edit_result.delete(0, tk.END)
            self.edit_result.insert(0, result_text)
            self._update_wallet_display()

        except ValueError as e:
            messagebox.showerror("Помилка введення", f"Перевірте коректність числових даних!\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyExchangeApp(root)
    root.mainloop()