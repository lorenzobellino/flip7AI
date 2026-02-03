from players import ProbabilisticAgent, RandomAgent, GAAgent, PointTresholdAgent
from flip7.objects import Flip7Game
import random
import os
import json


IMPORT_POPULATION = False
NUM_MATCHES = 20
POPULATION = 50
NUM_GENERATIONS = 150
OFFSPRING = 20
LOG_FREQ = 10

POPULATION_FILE = "populations/population_GA_v14.json"

def fitness(genome, verbose = False):

    opponent = RandomAgent(name="Random_Agent")
    # players = [GAAgent(genome=genome, name="GA_Agent"), RandomAgent(name="Random_Agent")]
 
    random_eval = evaluate([GAAgent(genome=genome, name="GA_Agent"), opponent], NUM_MATCHES, True, verbose)

    # opponent = PointTresholdAgent(treshold=30, name="Dumb_AI")
    # players = [GAAgent(genome=genome, name="GA_Agent"), opponent]
    # dumb_eval = evaluate(players, NUM_MATCHES, True, verbose)

    # opponent = ProbabilisticAgent(treshold=0.95, name="Prob_AI1")
    # players = [GAAgent(genome=genome, name="GA_Agent"), opponent]
    # probab_eval = evaluate(players, NUM_MATCHES, True)

    opponent = ProbabilisticAgent(treshold=0.19, name="Prob_AI19")

    prob2_eval = evaluate([GAAgent(genome=genome, name="GA_Agent"), opponent], NUM_MATCHES, True, verbose)

    # opponent = DumbPlayer(game)
    # dumb_eval = evaluate(game, agent, opponent, NUM_MATCHES)
    # game.reset()

    # opponent = RuleBasedPlayer(game)
    # rule_eval = evaluate(game, agent, opponent, NUM_MATCHES)

    # return (prob2_eval,dumb_eval, random_eval)  
    return (prob2_eval, random_eval)

def generate_population(dim: int) -> list:
    r = []
    for _ in range(dim):
        genome = {
            "alpha": random.uniform(-5, 5),
            "beta": random.uniform(-5, 5),
            # "ask_treshold": random.uniform(0, 1),
        }
        fit = fitness(genome)
        # print(f"Generated genome: {genome} with fitness: {fit}")
        # input()
        r.append((fit, genome))
    return r

def tournament(population, tournament_size=5):
    return max(random.choices(population, k=tournament_size), key=lambda i: i[0])


def combine(population, offspring):
    population += offspring
    population = sorted(population, key=lambda i: i[0], reverse=True)[:POPULATION]
    return population

def generate_offspring(population: list, gen: int) -> list:
    offspring = list()
    for _ in range(OFFSPRING):
        p = tournament(population)

        p[1]["alpha"] += random.gauss(0, 10 / (gen + 1))
        p[1]["beta"] += random.gauss(0, 10 / (gen + 1))
        # p[1]["gamma"] += random.gauss(0, 20 / (gen + 1))
        # p[1]["delta"] += random.gauss(0, 20 / (gen + 1))
        # p[1]["epsilon"] += random.gauss(0, 20 / (gen + 1))
        # p[1]["ask_treshold"] += random.gauss(0, 0.1 / (gen + 1))
        fit = fitness(p[1], verbose=False)
        # print(f"Generated offspring genome: {p[1]} with fitness: {fit}")
        # input()
        offspring.append((fit, p[1]))

    return offspring

def evaluate( players, n, infinite=True, verbose=False) -> float:
    """Evaluate the performance of a player against another player
    param:
        game: the game to be played
        players: list of players
        n: the number of matches to be played
    return:
        the ratio of matches won by GA_Agent
    """

    win_player0 = 0
    game = Flip7Game(players, infinite_deck=infinite)
    wins = {player.name: 0 for player in players}
    for _ in range(n):
        game.run()
        winner = max(game.players, key=lambda p: p.total_score)
        wins[winner.name] += 1
        if verbose:
            print(game)
            input()
        game.reset()

    result = wins["GA_Agent"]

    if verbose:
        print(f"Evaluation over {n} matches: {wins}")
        print(f"GA_Agent wins: {result} matches ({(result/n)*100:.2f}%)")
        print("------------------------------")
        input()

    # return percentage of wins of player1
    return wins["GA_Agent"] / n            


def GA():
    i = 0
    best_sol = None
    print("Starting GA")
    if IMPORT_POPULATION:
        with open(POPULATION_FILE, "r") as f:
            pop = json.load(f)
            population = [(fitness(p["genome"]), p["genome"]) for p in pop.values()]
            print(f"population imported")
    else:
        print(f"generating population of {POPULATION} individuals")
        population = generate_population(POPULATION)
        print(f"population generated")

    last_best_genome = ({},0)
    for _ in range(NUM_GENERATIONS):
        print(f"Generation {_}")
        offspring = generate_offspring(population, _)
        population = combine(population, offspring)
        print(f"best fitness: {population[0][0]}")
        print(f"best genome: {population[0][1]}")
        # Check for improvement
        if sum([population[0][1]["alpha"] == last_best_genome[0].get("alpha"),
             population[0][1]["beta"] == last_best_genome[0].get("beta")]) == 2:
            print(f"No improvement in best genome.")
            last_best_genome = (population[0][1], last_best_genome[1]+1)
        else:
            last_best_genome = (population[0][1], 1)
            print(f"New best genome found: {population[0][1]} with fitness: {population[0][0]}")

        if last_best_genome[1] >= 10:
            print(f"No improvement for 10 generations, performing larger mutation.")
            population[0][1]["alpha"] += random.gauss(0, 5)
            population[0][1]["beta"] += random.gauss(0, 5)
            
        # logging.debug(f"best genome: {population[0][1]}")
        # logging.debug(f"best fitness: {population[0][0]}")
        if (_ + 1) % LOG_FREQ == 0:
            if not os.path.exists("populations"):
                os.makedirs("populations")
            with open(f"populations/population_GA_v{i}.json", "w") as f:
                pop = {f"individual_{i:02}": {"fitness": p[0], "genome": p[1]} for i, p in enumerate(population)}
                json.dump(pop, f, indent=4)
                print(f"saved population")
            i += 1

    best_sol = population[0][1]
    return best_sol

def training():
    bes_genome = GA()
    agent = GAAgent(genome=bes_genome, name="GA_Agent_Best")
    opponents = [ProbabilisticAgent(treshold=0.95, name="Prob_AI_1"), ProbabilisticAgent(treshold=0.90, name="Prob_AI_2"),
                 RandomAgent(name="Random_AI")]
    players = [agent] + opponents
    game = Flip7Game(players, infinite_deck=True)
    game.run()



if __name__ == "__main__":
    training()
