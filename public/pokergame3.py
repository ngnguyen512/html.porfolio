import random
import sys
from collections import Counter, defaultdict
from graphics import *


class Card:
    Ranks = list("23456789TJQKA")
    Suits = list("HDCS")
    Suitsymbol = {"C": chr(9827), "D" : chr(9830), "H" : chr(9829), "S": chr(9824)}

    def __init__(self, rank, suit):
        if not (rank in Card.Ranks) or not (suit in Card.Suits):
            raise ValueError("Check your ranks and suits")
        else:
            self.rank = rank
            self.suit = suit
            self.face_up = False
        
    def __str__(self):
            return str(self.rank) + Card.Suitsymbol[self.suit]
    
    def draw_face_down(self, win, pt):
        self.height = 2
        self.width = 0.6 * self.height
        self.rect = Rectangle(pt, Point(pt.getX() + self.width, pt.getY() + self.height))
        self.rect.setFill('gray')
        self.rect.draw(win)
        
    
    def draw_face_up(self, win, pt):
        self.height = 2
        self.width = 0.6 * self.height
        self.rect = Rectangle(pt, Point(pt.getX() + self.width, pt.getY() + self.height))
        self.rect.setFill('white')
        self.rect.draw(win)
        self.text = Text(self.rect.getCenter() , self.rank + self.Suitsymbol[self.suit])
        self.text.setSize(20)
        if self.suit == "H" or self.suit == "D":
            self.text.setTextColor("red")
        else:
            self.text.setTextColor("black")
        self.text.draw(win)

    def undraw(self):
        self.rect.undraw()
        self.text.undraw()
    
    def getRank(self):
        return self.rank
    
    def getSuit(self):
        return self.suit

class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, 'Quit') """ 

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()
    
    def draw(self, win):
        self.rect.draw(win)
        self.label.draw(win)

    def undraw(self):
        self.rect.undraw()
        self.label.undraw()

    def clicked(self, p):
        "Returns true if button active and p is inside"
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.rect.setFill('yellow')
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
        
    def create_deck(self):
        for suit in Card.Suits:
            for rank in Card.Ranks:
                self.cards.append(Card(rank, suit))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) == 0:
            raise ValueError("No more cards in the deck.")
        return self.cards.pop()
    
    def __len__(self):
        return len(self.cards)


class PokerHand:
    hand_rankings = [
        "Straight Flush",
        "Four of a Kind",
        "Full House",
        "Flush",
        "Straight",
        "Three of a Kind",
        "Two Pair",
        "One Pair",
        "High Card"
    ] 
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def check_hand(self, table_cards):
        all_cards = self.cards + table_cards
        ranks = [card.rank for card in all_cards]
        suits = [card.suit for card in all_cards]

        # Check from highest rank to lowest
        if self.check_straight_flush(suits, ranks):
            return "Straight Flush"
        elif self.check_four_kind(ranks):
            return "Four of a Kind"
        elif self.check_full_house(ranks):
            return "Full House"
        elif self.check_flush(suits):
            return "Flush"
        elif self.check_straight(ranks):
            return "Straight"
        elif self.check_three_kind(ranks):
            return "Three of a Kind"
        elif self.check_two_pairs(ranks):
            return "Two Pair"
        elif self.check_one_pair(ranks):
            return "One Pair"
        else:
            return "High Card"
    
    def check_straight_flush(self, suits, ranks):
        # Get all suits and ranks
        all_suits = ['H', 'D', 'C', 'S']
        all_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        # Check each suit
        for suit in all_suits:
            # Get ranks of cards with this suit
            suited_ranks = [rank for rank, s in zip(ranks, suits) if s == suit]

            if self.check_straight(suited_ranks):
              return True

        return False

        
    def check_straight(self, ranks):
        if (len(ranks)) < 5:
            return False
        all_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        rank_indicies = sorted(set(all_ranks.index(rank) for rank in ranks))
        for i in range(len(rank_indicies) - 4):
          start = rank_indicies[i]
          if rank_indicies[i:i+5] == [start, start+1, start+2, start+3, start+4]:
            return True 

        return False

    def check_four_kind(self, ranks):
        rank_count = Counter(ranks)
        return 4 in rank_count.values()

    def check_three_kind(self, ranks):
        rank_count = Counter(ranks)
        return 3 in rank_count.values()

    def check_full_house(self, ranks):
        rank_count = Counter(ranks)
        return 2 in rank_count.values() and 3 in rank_count.values()

    def check_flush(self, suits):
        suit_count = Counter(suits)
        return 5 in suit_count.values()

    def check_two_pairs(self, ranks):
        rank_count = Counter(ranks)
        return list(rank_count.values()).count(2) >= 2

    def check_one_pair(self, ranks):
        rank_count = Counter(ranks)
        return 2 in rank_count.values()
        
    def get_pair_rank(self, table_cards):
        rank_count = Counter([card.rank for card in self.cards + table_cards])
        pairs = [rank for rank, count in rank_count.items() if count == 2]
        if pairs:
            all_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
            pair_ranks = sorted(pairs, key=all_ranks.index)
            return pair_ranks[0]

    def get_high_card(self):
        all_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        card_ranks = sorted([card.rank for card in self.cards], key=all_ranks.index)
        return card_ranks[0]
    
class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer_hole = PokerHand()
        self.player_hole = PokerHand()
        self.table_cards = []
        self.betting_round = 1
        self.controls = {
            'STAY': self.stay,
            'FOLD': self.fold,
            'DEAL': self.deal_initial_cards,
            'QUIT': self.quit
        }
        self.results = {
            "average point" :0,
            "games_played": 0 }
        self.deal_initial_cards()
        self.folded_round = 0
        self.score = 0
        self.win = GraphWin("Poker Solitaire", 600, 600)
        self.win.setCoords(0, 0, 10, 10)
        self.controlText = Text(Point(8.5, 7.5), "CONTROLS")
        self.controlText.draw(self.win)
        self.controls_box = Rectangle(Point(7, 7.9), Point(10, 10)) 
        self.controls_box.draw(self.win)
        self.controls_text = Text(self.controls_box.getCenter(), "")
        self.controls_text.draw(self.win)
        self.dealText = Text(Point(1.5, 7.5), "DEALER'S HOLE")
        self.dealText.draw(self.win)
        self.playText = Text(Point(8.5, 3.5), "PLAYER'S HOLE")
        self.playText.draw(self.win)
        self.resultText = Text(Point(1.5, 3.5), "RESULTS")
        self.resultText.draw(self.win)
        self.results_box = Rectangle(Point(0, 0), Point(3.5, 3.2)) 
        self.results_box.draw(self.win)
        self.results_text = Text(self.results_box.getCenter(), "")
        self.results_text.draw(self.win)
        self.winner_point = Point(1.75, 2.9)
        self.loser_point = Point(1.75, 2.4)
        self.action_point = Point(1.75, 1.9)
        self.sc_point = Point(1.75, 1.4)
        self.av_point = Point(1.75, 1)
        self.results_text_winner = Text(self.winner_point, "")
        self.results_text_winner.setTextColor("red")
        self.results_text_winner.setSize(15)
        self.results_text_loser = Text(self.loser_point, "")
        self.results_text_loser.setTextColor("blue")
        self.results_text_loser.setSize(15)
        self.results_text_action = Text(self.action_point, "")
        self.results_text_action.setSize(15)
        self.results_text_score = Text(self.sc_point, "")
        self.results_text_score.setSize(15)
        self.results_text_average = Text(self.av_point, "")
        self.results_text_average.setSize(10)
        self.quit_button = Button(self.win, Point(9.3, 9.5), 1, 0.8, 'QUIT')
        self.deal_button = Button(self.win, Point(8, 9.5), 1, 0.8, 'DEAL')
        self.stay_button = Button(self.win, Point(8, 8.5), 1, 0.8, 'STAY')
        self.fold_button = Button(self.win, Point(9.3, 8.5), 1, 0.8, 'FOLD')
        self.action = " "
        self.game_played = 1
        self.sum_point = 0
        self.stay_button.activate()
        self.fold_button.activate()
    
    def draw_player_cards(self):
        x = 7
        y = 1
        for card in self.player_hole.cards:
            card.draw_face_up(self.win, Point(x, y))
            x += 1.5
    def draw_dealer_cards(self, face_up=False):
        x = 0.3
        y = 7.8
        for card in self.dealer_hole.cards:
            if face_up:
                card.draw_face_up(self.win, Point(x, y))
            else:
                card.draw_face_down(self.win, Point(x, y))
            x += 1.5
    
    def draw_table_cards(self,face_down=True):
        x = 3
        y = 4.5
        for i, card in enumerate(self.table_cards[0:3]):
            if face_down:
                card.draw_face_down(self.win, Point(x + i * 1.5, y))
            else:
                card.draw_face_up(self.win, Point(x + i * 1.5, y))
        if face_down:
            self.table_cards[3].draw_face_down(self.win, Point(4.5, 7))
        else:
            self.table_cards[3].draw_face_up(self.win, Point(4.5, 7))
        if face_down:
            self.table_cards[4].draw_face_down(self.win, Point(4.5, 2))
        else:
            self.table_cards[4].draw_face_up(self.win, Point(4.5, 2))
    def reveal_first_three_table_cards(self):
        x = 3
        y = 4.5
        for i, card in enumerate(self.table_cards[0:3]):
                card.draw_face_up(self.win, Point(x + i * 1.5, y))
    def reveal_fourth_card(self):
        self.table_cards[3].draw_face_up(self.win, Point(4.5, 7))
    def reveal_fifth_card(self):
        self.table_cards[4].draw_face_up(self.win, Point(4.5, 2))

    def deal_initial_cards(self):
        for _ in range(2):
            self.dealer_hole.add_card(self.deck.deal())
            self.player_hole.add_card(self.deck.deal())
        for _ in range(5):
            self.table_cards.append(self.deck.deal())
        
    def stay(self):
        self.action += "S/"
        if self.betting_round == 1:
            self.reveal_first_three_table_cards()
            """self.next_betting_round()"""
        elif self.betting_round == 2:
            self.reveal_fourth_card()
            """self.next_betting_round()"""
        elif self.betting_round == 3:
            self.reveal_fifth_card()
            """self.next_betting_round()"""
        elif self.betting_round == 4:
            self.sum_point += self.evaluate_and_results()
            print("Dealer's hole:",[f'{card.rank}{card.suit}' for card in self.dealer_hole.cards])
            self.draw_dealer_cards(True)
            self.deal_button.activate()
            self.quit_button.activate()
            self.stay_button.deactivate()
            self.fold_button.deactivate()
            self.results_text_winner.draw(self.win)
            self.results_text_loser.draw(self.win)
            self.results_text_action.draw(self.win)
            self.results_text_score.draw(self.win)
            self.results_text_average.draw(self.win)
        self.next_betting_round()

    def fold(self):
        print("Dealer's hole:",[f'{card.rank}{card.suit}' for card in self.dealer_hole.cards])
        self.draw_dealer_cards(True)
        self.draw_table_cards(False)
        self.folded_round = self.betting_round
        print("Table cards:", [f'{card.rank}{card.suit}' for card in self.table_cards])
        self.action += "F"
        self.score = self.evaluate_and_results()
        self.sum_point += self.evaluate_and_results()
        self.results_text_winner.draw(self.win)
        self.results_text_loser.draw(self.win)
        self.results_text_action.draw(self.win)
        self.results_text_score.draw(self.win)
        self.results_text_average.draw(self.win)
        self.deal_button.activate()
        self.quit_button.activate()
        self.stay_button.deactivate()
        self.fold_button.deactivate()
        self.betting_round = 0
        
    def deal_table_cards(self, n):
        for _ in range(n):
            self.table_cards.append(self.deck.deal())
    
    def print_game(self):
        print("Round:", self.betting_round)
        print("Dealer's hole:",[f'{card.rank}{card.suit}' for card in self.dealer_hole.cards])
        print("Player's hole:", [f'{card.rank}{card.suit}' for card in self.player_hole.cards])
        print("Table cards:", [f'{card.rank}{card.suit}' for card in self.table_cards])
        
    def quit(self):
        print("Quitting the game.")
        sys.exit()

    def next_betting_round(self):
        self.betting_round += 1
        if self.betting_round <=4:
            self.stay_button.activate()
            self.fold_button.activate()
        if self.betting_round > 4:
            self.betting_round = 0
            self.results['games_played'] += 1
            self.evaluate_and_results()
    
    def evaluate_and_results(self):
        all_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        Dealer_result = self.dealer_hole.check_hand(self.table_cards)
        Player_result = self.player_hole.check_hand(self.table_cards)
        print("Dealer's hole: ", Dealer_result)
        print("Player's hole: ", Player_result)
        if Dealer_result == Player_result:
            if Dealer_result == "One Pair":
                dealer_pair_rank = self.dealer_hole.get_pair_rank(self.table_cards)
                player_pair_rank = self.player_hole.get_pair_rank(self.table_cards)
                dealer_pair_rank_index = all_ranks.index(dealer_pair_rank)
                player_pair_rank_index = all_ranks.index(player_pair_rank)
                if dealer_pair_rank and player_pair_rank and dealer_pair_rank_index < player_pair_rank_index :
                    print("Dealer wins!")
                    self.results_text_winner.setText(f"√Dealer: {Dealer_result}")
                    self.results_text_loser.setText(f"Player: {Player_result}")
                    game_points = -100
                elif dealer_pair_rank and player_pair_rank and dealer_pair_rank_index == player_pair_rank_index:
                    self.results_text_winner.setText(f"It's a draw")
                    game_points = 0
                else:
                    self.results_text_winner.setText(f"√Player: {Player_result}")
                    self.results_text_loser.setText(f"Dealer: {Dealer_result}")
                    game_points = 100
            elif Dealer_result == "High Card":
                dealer_high_card = self.dealer_hole.get_high_card()
                player_high_card = self.player_hole.get_high_card()
                dealer_high_card_index = all_ranks.index(dealer_high_card)
                player_high_card_index = all_ranks.index(player_high_card) 
                if dealer_high_card and player_high_card and dealer_high_card_index < player_high_card_index:
                    print("Dealer wins!")
                    self.results_text_winner.setText(f"√Dealer: {Dealer_result}")
                    self.results_text_loser.setText(f"Player: {Player_result}")
                    game_points = -100
                elif dealer_high_card and player_high_card and dealer_high_card_index == player_high_card_index:
                    self.results_text_winner.setText(f"It's a draw")
                    game_points = 0
                else:
                    print("Player wins!")
                    self.results_text_winner.setText(f"√Player: {Player_result}")
                    self.results_text_loser.setText(f"Dealer: {Dealer_result}")
                    game_points = 100
            else:
                self.results_text_winner.setText("It's a draw")
                self.results_text_loser.setText("")
                print("It's a draw!")
                game_points = 0
        else:
            if PokerHand.hand_rankings.index(Dealer_result) < PokerHand.hand_rankings.index(Player_result):
                print("Dealer wins!")
                self.results_text_winner.setText(f"√Dealer: {Dealer_result}")
                self.results_text_loser.setText(f"Player: {Player_result}")
                game_points = -100
            else:
                print("Player wins!")
                self.results_text_winner.setText(f"√Player: {Player_result}")
                self.results_text_loser.setText(f"Dealer: {Dealer_result}")
                game_points = 100
        
        self.results_text_action.setText(f"Action: {self.action}")
        
        if self.folded_round:
            fold_points = 100 - (self.folded_round - 1) * 25
            if game_points < 0: 
                game_points = fold_points
            elif game_points > 0:  
                game_points = -fold_points

        print(f"Score for this round: {game_points}")
        self.results_text_score.setText(f'Score for this round: {game_points}')
        self.results_text_average.setText(f'AVG: {round(self.sum_point/self.game_played, 1)} out of {self.game_played}')
        return game_points

    def reset_game(self):
        self.dealer_hole = PokerHand()
        self.player_hole = PokerHand()
        self.table_cards = []
        self.deck = Deck()
        self.deck.shuffle()
        self.betting_round = 1
        self.folded_round = 0
        self.deal_initial_cards()
        self.action = " "
        self.game_played += 1
        self.results_text_winner.undraw()
        self.results_text_loser.undraw()
        self.results_text_action.undraw()
        self.results_text_score.undraw()
        self.results_text_average.undraw()
        self.deal_button.deactivate()
        self.quit_button.deactivate()
        self.stay_button.activate()
        self.fold_button.activate()
        self.draw_player_cards()
        self.draw_dealer_cards(False)
        self.draw_table_cards(True)
    
    def handle_button_click(self):
        click_point = self.win.getMouse()
        # Get the mouse click point

    # Check if each button was clicked and perform the appropriate action
        if self.stay_button.clicked(click_point):
            self.stay()
        elif self.fold_button.clicked(click_point):
            self.fold()
        elif self.deal_button.clicked(click_point):
            self.stay_button.deactivate()
            self.fold_button.deactivate()
            self.reset_game()
        elif self.quit_button.clicked(click_point):
            self.quit()

def main():
    game = PokerGame()
    game.draw_player_cards()
    game.draw_dealer_cards()
    game.draw_table_cards()
    
    while True:
        if game.betting_round != 0:
            print("Round:", game.betting_round)
            print("Dealer's hole:",[f'{card.rank}{card.suit}' for card in game.dealer_hole.cards])
            print("Player's hole:", [f'{card.rank}{card.suit}' for card in game.player_hole.cards])
            print("Table cards:", [f'{card.rank}{card.suit}' for card in game.table_cards])
        game.handle_button_click()
if __name__ == "__main__":
    main()