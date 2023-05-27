import random

class Simulation:
    """Initialize the Monty Hall simulation with the number of doors."""
    def __init__(self, doornum):
        self.numdoors = doornum

    def set_random_doors(self):
        """Create a list of doors with one car behind a random door and zonks behind the rest."""
        doors = ["zonk"] * self.numdoors
        car_index = random.randint(0, self.numdoors - 1)
        doors[car_index] = "car"
        return doors

    def choose_doors(self):
        """Choose an initial door and an alternate door after removing a zonk."""
        doors = self.set_random_doors()
        chosen_door = doors.pop(random.randint(0, len(doors) - 1))
        if "zonk" in doors:
            doors.remove("zonk")
        alternate_door = doors.pop(random.randint(0, len(doors) - 1))
        return (chosen_door, alternate_door)

    def play_game(self, switch=False, iterations=1):
        """
               Play the Monty Hall game with the option to switch doors.

               Args:
                   switch (bool): Whether to switch doors or not. Default is False.
                   iterations (int): Number of times to play the game. Default is 1.

               Return:
                   float: The win percentage after playing the game for the given number of iterations.
        """
        wins = 0
        for _ in range(iterations):
            chosen_door, alternate_door = self.choose_doors()
            if (chosen_door == "car" and not switch) or (alternate_door == "car" and switch):
                wins += 1
        return wins / iterations

if __name__ == "__main__":
    sim = Simulation(3)
    win_percentage = sim.play_game(switch=True, iterations=1000)
    print(win_percentage)
