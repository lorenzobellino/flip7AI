from flip7.objects import Player


class HumanPlayer(Player):

    def __init__(self, name="HumanPlayer", verbose = False):
        super().__init__()
        self.name = name
        self.verbose = verbose
        self.second_chance = True

    def ask_card(self, game) -> bool:
        print(f"Your hand: {self.hand} | Current score: {self.count_score()} | Total score: {self.total_score} | Second Chance: {self.second_chance}")
        while True:
            choice = input("Do you want to ask for another card? (y/n): ").strip().lower()
            if choice in ['y', 'n']:
                res = choice == 'y'
                if self.verbose:
                    if res:
                        print(f"{self.name} chose to ask for another card.")
                    else:
                        print(f"{self.name} chose to stop asking for cards.")
                return choice == 'y'
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    def __repr__(self):
        return f"{self.name}"

    def choose_to_flip3(self, players):
        print("Choose a player to flip 3 cards:")
        for idx, player in enumerate(players):
            if player != self:
                print(f"{idx}: {player.name} (Total score: {player.total_score})")
        while True:
            try:
                choice = int(input("Enter the number of the player you want to flip 3 cards to: "))
                if 0 <= choice < len(players) and players[choice] != self:
                    return players[choice]
                else:
                    print("Invalid choice. Please choose a valid player number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def choose_to_freeze(self, players):
        print("Choose a player to freeze:")
        for idx, player in enumerate(players):
            if player != self:
                print(f"{idx}: {player.name} (Total score: {player.total_score})")
        while True:
            try:
                choice = int(input("Enter the number of the player you want to freeze: "))
                if 0 <= choice < len(players) and players[choice] != self:
                    return players[choice]
                else:
                    print("Invalid choice. Please choose a valid player number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    
    def reset(self):
        input(f"End of round. Your total score is {self.total_score}. Press Enter to continue...")
        super().reset()
        self.second_chance = True

    