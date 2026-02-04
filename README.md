# Flip 7 AI



    # def learn(self, win: bool) -> None:
    #     for board, value in self.current_state.items():
    #         # current_state = {board: {"piece": [[piece, score], ..], "move": [[move, score], ..]}}
    #         flag = False
    #         if board in self.G:  # if the board is in the policy
    #             # if the update is for a piece
    #             if "piece" in value and "piece" in self.G[board]:
    #                 for p in self.G[board]["piece"]:  # self.G[board]["piece"] = [[piece, score], ..]
    #                     if p[0] == value["piece"]:
    #                         if win:
    #                             p[1] += 1  # if win increase the score by 1
    #                         else:
    #                             p[1] -= 1  # if lose decrease the score by 1
    #                         flag = True
    #                         break
    #                 if not flag:  # if the piece is not in the policy add it
    #                     self.G[board]["piece"].append([value["piece"], 1 if win else -1])
    #             # if the update is for a move
    #             elif "move" in value and "move" in self.G[board]:
    #                 for p in self.G[board]["move"]:  # self.G[board]["move"] = [[move, score], ..]
    #                     if p[0] == value["move"]:
    #                         if win:
    #                             p[1] += 1  # if win increase the score by 1
    #                         else:
    #                             p[1] -= 1  # if lose decrease the score by 1
    #                         flag = True
    #                         break
    #                 if not flag:  # if the move is not in the policy add it
    #                     self.G[board]["move"].append([value["move"], 1 if win else -1])
    #         else:  # if the board is not in the policy
    #             if "piece" in value:
    #                 self.G[board] = {"piece": [[value["piece"], 1 if win else -1]]}  # add a new entry for the piece
    #             elif "move" in value:
    #                 self.G[board] = {"move": [[value["move"], 1 if win else -1]]}  # add a new entry for the move

    #     self.current_state = dict()  # reset the current state
    #     self.randomness -= self.learning_rate  # decrease the randomness