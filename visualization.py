import monty_hall
import pandas as pd
import seaborn as sns


class Plot:
    def __init__(self, doors=3, iterations=200):
        """
               Initialize the Plot class for the Monty Hall simulation.

               Argss:
                   doors (int): Number of doors in the Monty Hall game. Default is 3.
                   iterations (int): Number of iterations to run the simulation. Default is 200.
        """
        self.doors = doors
        self.iterations = iterations
        self.sequence = []

        for i in range(1, self.iterations + 1):
            sim = monty_hall.Simulation(self.doors)
            switch = i % 2 == 0
            win_percentage = sim.play_game(switch=switch, iterations=i)
            self.sequence.append(
                {"iterations": i, "percentage": win_percentage, "doors": self.doors, "switched": str(switch)})

        self.make_plot()

    def make_plot(self):
        """Generate a plot of win percentages for the Monty Hall simulation."""
        df = pd.DataFrame(self.sequence)
        plot = sns.lmplot(x="iterations", y="percentage", data=df, hue="switched")
        plot.savefig(f"monty_hall_doors_{self.doors}_iterations_{self.iterations}.png")


if __name__ == "__main__":
    plot_instance = Plot(doors=5, iterations=100)
