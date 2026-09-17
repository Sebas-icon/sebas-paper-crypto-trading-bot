plot_profit.py` -> paste this -> COMMIT:
plot_profit.py - Plot P/L from trades.csv
import csv
import matplotlib.pyplot as plt

timestamps = []
balances = []

try:
    with open("trades.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["event"].startswith("SELL") or row["event"] == "PRICE":
                try:
                    timestamps.append(row["timestamp"][-8:]) # HH:MM:SS
                    balances.append(float(row["balance"]))
                except:
                    pass

    plt.figure()
    plt.plot(balances, marker='o')
    plt.title("Sebas Paper Bot - Balance Over Time")
    plt.xlabel("Ticks")
    plt.ylabel("Balance USD")
    plt.grid(True)
    plt.savefig("profit.png")
    print("Saved profit.png")
except FileNotFoundError:
    print("No trades.csv yet - run main.py first")
except Exception as e:
    print(f"Error: {e}")