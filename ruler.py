from card import Card
from player import Player
import random

class Ruler:
    def __init__(self,N,H):
        self.game_done = False
        self.turn = 0
        self.cycle_num = 0
        self.winner = []
        self.total_player_num = N
        self.human_player_num = H
        self.player_list = [] # list of players who play the game.
        self.init_card_set = []
        self.recent_card = None
        self.last_submit_player = None

    def init_game(self):
        self.create_players()
        self.make_card_set()
        self.give_card_set()

    def create_players(self):
        for computer in range(self.total_player_num-self.human_player_num):
            self.player_list.append(Player('computer'+str(computer+1)))
        for human in range(self.human_player_num):
            name = input('Please enter the name of player '+str(human+1)+' : ')
            self.player_list.append(Player(name, True))

        # shuffle it.
        random.shuffle(self.player_list)
        print('All players are created.')

    def make_card_set(self):
        for i in range(12):
            for j in range(i+1):
                self.init_card_set.append(Card(str(i+1),str(i+1)))

        # two Js.
        self.init_card_set.append(Card('13','13'))
        self.init_card_set.append(Card('13','13'))

        # shuffle it.
        random.shuffle(self.init_card_set)

    def give_card_set(self):
        for i in range(80):
            code = (i+1)%self.total_player_num
            self.player_list[code].card_list.append(self.init_card_set[i])

        print('All cards are given.')

    # Functions for the game.
    def are_you_done(self, player):
        if len(player.card_list) == 0:
            self.winner.append(player.name)
            #self.player_list.remove(player)
            return True
        return False

    def determine_next_turn(self):
        if self.now_player.limit_level == 3: # if now player call 'die',
            # For every case except following one, keep the turn number.
            # Exception: when now_player is the last player in the possible_player list. -> turn should be 0.
            if self.turn == len(self.possible_player): self.turn = 0

        else:
            if self.fin:  # if now_player have done the game.
                # Record the index of the player. It will be used for a specific case.
                # Remove the player from the list.
                self.player_list.remove(self.now_player)
                # For every case except following one, keep the turn number.
                # possible_player still contain the player who have done the game.
                # Therefore, subtract 1 from len to get max possible turn number.
                if self.turn == (len(self.possible_player) - 1): self.turn = 0
            else:
                if self.turn + 1 < len(self.possible_player):
                    self.turn += 1
                else:
                    self.turn = 0

    def next_play(self):
        # initial possible players
        self.possible_player = [player for player in self.player_list if player.limit_level != 3]
        self.now_player = self.possible_player[self.turn]

        if self.recent_card == None:
            self.now_player.limit_level = 1

        if self.now_player.limit_level != 3:  # this person already die.
            if self.now_player.human:
                self.now_player.do_game(self.recent_card)
            else:
                self.now_player.auto_game(self.recent_card)

            # change recent_card only if player does not call 'die'.
            if self.now_player.limit_level != 3:
                self.recent_card = self.now_player.submitted_card
                self.last_submit_player = self.now_player
                self.last_submit_player_index = self.player_list.index(self.now_player)

        # check whether now_player have done the game.
        self.fin = self.are_you_done(self.now_player)

        # update possible players
        self.possible_player = [player for player in self.player_list if player.limit_level != 3]

        # determine next player.
        self.determine_next_turn()

    def next_cycle(self):
        # Very Very specific case. Assume four players, [a,b,c,d]. a and c already die and it d's turn.
        # Here, 'd' finished tha game! Then what happened?
        # First, the turn goes to 'b'. 'b' can do two things. Give a correct card(s) or call die.
        # In case of giving the correct card(s), len(possible_player) = 1 with containing 'b'.
        # It's the beginning of a new cycle. However, in case of calling die, it cause a problem.
        # Then len(possible_player) = 0 with nothing. We should back the turn to right next player of 'd', 'a'.
        # To do that, I recorded previous_player's index in player_list before remove it.
        if len(self.possible_player) == 0:
            if self.last_submit_player_index == len(self.player_list):
                self.turn = 0
            else:
                self.turn = self.last_submit_player_index
            self.recent_card = None
            self.cycle_num += 1
            for player in self.player_list:
                player.limit_level = 2

        # General cases (len(possible_player) = 1)
        else:
            if self.last_submit_player == self.possible_player[0]:
                self.recent_card = None
                self.cycle_num += 1
                for player in self.player_list:
                    if player.limit_level == 2:
                        self.turn = self.player_list.index(player)
                    else: player.limit_level = 2




