from random import shuffle
from IPython.display import clear_output
import gc

class Deck():

    maindeck = []
    suits = ('H','D','S','C')
    val_card = (2,3,4,5,6,7,8,9,10,'J','Q','K','A')
    cardsCounter = []

    def fullDeck(self):
        
        for i in range(0,4):
            for j in range(0,13):
                self.maindeck.append([self.val_card[j],self.suits[i]])

    def cardsCount(self):
        return sum(self.cardsCounter)

class Table(Deck):

    cardsInMyHand = []
    cardsInDillerHand = []
    myHandSum = 0
    dillerHandSum = 0

    def pullingOutCardsStart(self):
        self.cardsInMyHand.append(self.maindeck[-1])
        self.cardsInMyHand.append(self.maindeck[-3])
        self.cardsInDillerHand.append(self.maindeck[-2])
        self.cardsInDillerHand.append(self.maindeck[-4])
        for _ in range(0,4):
            self.cardsCounter.append(1)
            self.maindeck.pop()

    def showCards(self):
        print("Cards in your hand:")
        for i in self.cardsInMyHand:
            print(i)
        print("Cards in diller's hand:")
        print(f"{self.cardsInDillerHand[0]} and another one.")

    def hit(self):
        self.cardsInMyHand.append(self.maindeck[-1])
        self.cardsCounter.append(1)
        self.maindeck.pop()

    def dillerHit(self):
        self.cardsInDillerHand.append(self.maindeck[-1])
        self.cardsCounter.append(1)
        self.maindeck.pop()

    def clearHands(self):
        self.cardsInMyHand.clear()
        self.cardsInDillerHand.clear()

class Hands(Table):

    def mySum_vals(self):
        self.handSum = 0
        for i in range(len(self.cardsInMyHand)):
            if self.cardsInMyHand[i][0] in ['J', 'Q', 'K']:
                self.handSum += 10
            elif self.cardsInMyHand[i][0] == 'A':
                self.handSum += 11
                if self.handSum > 21:
                    self.handSum -= 11
                    self.handSum += 1
                else:
                    pass
            else:
                self.handSum += self.cardsInMyHand[i][0]
        return self.handSum
    
    def dillerSum_vals(self):
        self.dillerHandSum = 0
        for i in range(len(self.cardsInDillerHand)):
            if self.cardsInDillerHand[i][0] in ['J', 'Q', 'K']:
                self.dillerHandSum += 10
            elif self.cardsInDillerHand[i][0] == 'A':
                self.dillerHandSum += 11
                if self.dillerHandSum > 21:
                    self.dillerHandSum -= 11
                    self.dillerHandSum += 1
                else:
                    pass
            else:
                self.dillerHandSum += self.cardsInDillerHand[i][0]
        return self.dillerHandSum

class Chip():

    rep = []
    amount = 0
    bet = 0

    def betting(self):
        if self.rep[0] < self.bet:
            raise NotImplementedError("Not enough chips error!")
        else:
            self.rep[0] -= self.bet
            print(f"Your bet is {self.bet}.")

    def draw(self):
        self.rep[0] += self.bet
    
    def win(self):
        self.rep[0] += self.bet * 2

    def amountFix(self):
        self.rep.append(self.amount)

    def replayOrNot(self):
        return len(self.rep) == 0

    def __str__(self):
        return self.amount

def main_game():
    
    deck = Deck()
    table = Table()
    s = Hands()
    chip = Chip()

    deck.fullDeck()
    shuffle(deck.maindeck)
    
    while True:
        if chip.replayOrNot() != True:
            chips = chip.rep[0]
            break

        try:
            chips = int(input("How many chips you got?"))
        except:
            print("Enter the number!")
        else:
            chip.amount = chips
            chip.amountFix()
            chips = chip.rep[0]
            break    
    
    while True:
        try:
            bet_game = int(input("What is your bet?"))           
        except NotImplementedError:
            print("Not enough chips!")
        except:
            print("Enter the number!")
        else:
            chip.bet = bet_game
            chip.betting()
            break

    clear_output()
    table.pullingOutCardsStart()
    table.showCards()
    
    if s.mySum_vals() == 21:
        stay = True
    else:
        stay = False
    
    while not stay:
        try:
            choice_player = int(input(f'Your hand is {s.mySum_vals()}. Hit(1) or Stay(2)?'))
        except:
            print("Enter the number!")
        if choice_player == 1:
            table.hit()
            clear_output()
            table.showCards()
            if s.mySum_vals() > 21:
                break
            elif s.mySum_vals() == 21:
                stay = True
            continue
        else:
            stay = True

    clear_output()
    print(f'Your hand is {s.mySum_vals()}')

    while s.dillerSum_vals() < 17:
        table.dillerHit()
        s.dillerSum_vals()

    print(f"Diller's hand is {s.dillerSum_vals()}")

    if (s.dillerSum_vals() > 21 and s.mySum_vals() <= 21) or (s.dillerSum_vals() < 21 and s.mySum_vals() <= 21 and (s.mySum_vals() > s.dillerSum_vals())):
        chip.win()
        print(f'You win {bet_game*2}!')
    elif (s.dillerSum_vals() == s.mySum_vals()) or (s.dillerSum_vals() > 21 and s.mySum_vals() > 21):
        chip.draw()
        print(f'Draw. You got {bet_game} back.')
    else:
        print(f'You lost {bet_game}.')

    print(f'Currently you have {chip.rep[0]} chips.')

    table.clearHands()
    deck.maindeck = []
    table.cardsInMyHand = []
    table.cardsInDillerHand = []

    del deck
    del table
    del s
    del chip

    gc.collect()

if __name__ == '__main__':
    deck = Deck()
    while True:
        main_game()
        if 36 <= deck.cardsCount() <= 56:
            print('Reshuffle is needed.\nThanks for playing!')
            break
        replay = input("Want to play again?")
        if replay in ['Y', 'y', 'Yes', 'yes']:
            q = 0
            continue
        else:
            print('Thanks for playing!')
            break