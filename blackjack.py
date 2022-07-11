from re import X
import requests


def generate_deck(count):
    response = requests.post(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={count}")
    data = response.json()
    deckid = data['deck_id']
    return deckid

def draw_card(deckid, cards):
    response = requests.post(f"https://deckofcardsapi.com/api/deck/{deckid}/draw/?count={cards}")
    data = response.json()
    return data

def return_card(deckid, card):
    requests.post(f"https://deckofcardsapi.com/api/deck/{deckid}/return/?cards={card}")
    return None

def reshuffle(deckid):
    requests.post(f"https://deckofcardsapi.com/api/deck/{deckid}/shuffle")
    return 0

def convert(data):
    if data[0] == 'A':
        return 11
    if data[0] == 'K':
        return 10
    if data[0] == 'Q':
        return 10
    if data[0] == 'J':
        return 10
    if data[0] == '0':
        return 10
    else:
        return int(data[0])

def count(x):
    if x < 7:
        return(1)
    elif x > 9:
        return(-1)
    else:
        return(0)

#d31xyjxoan40

def manual_play():
    money_to_bet = input("Enter starting money:")
    while not money_to_bet.isdigit():
            print("\nPlease enter a number")
            money_to_bet = input("Enter starting money:")
    money_to_bet = int(money_to_bet)
    deck_id = generate_deck(1)
    game = 1
    deck_count = 0
    while True:
        # check deck size at start of round
        card = draw_card(deck_id, 1)
        if card['remaining'] <= 10:
            deck_count = reshuffle(deck_id)
            print("Deck reshuffled") 
        return_card(deck_id, card['cards'][0]['code'])   

        # running game count
        print(f"Game: {game}")
        game += 1

        # running card count
        print("Deck Strength: ", deck_count)
        bet = input("Enter Bet:")
        while not bet.isdigit():
            print("\nError, please enter a number")
            bet = input("Enter Bet:")
        while int(bet) < 10:
            print("\nThe house minimum bet is 10, please try again")
            bet = input("Enter Bet:")

        # play a hand
        print("\nEnter 1 to draw")
        print("Enter any key to exit\n")
        x = input()
        if x == "1":
            # player draw
            player_hand_count = 0
            # first card
            card = draw_card(deck_id, 1)
            player_hand_count += convert(card['cards'][0]['code'])
            deck_count += count(convert(card['cards'][0]['code']))
            # second card
            card = draw_card(deck_id, 1)
            player_hand_count += convert(card['cards'][0]['code'])
            deck_count += count(convert(card['cards'][0]['code']))

            # hit loop
            while True:
                print(f"Hand Strength: {player_hand_count}")
                print("Enter 1 to hit")
                print("Enter any key to stay\n")
                if input() == "1":
                    card = draw_card(deck_id, 1)
                    player_hand_count += convert(card['cards'][0]['code'])
                    deck_count += count(convert(card['cards'][0]['code']))
                else:
                    break 
            # condition when player bust, dealer hand still played
            if player_hand_count > 21:
                print("Dealer Wins !\n\n")
                money_to_bet -= int(bet)
                print("Current Wallet:", money_to_bet)
                dealer_hand_count = 0
                #first card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                deck_count += count(convert(card['cards'][0]['code']))
                #second card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                deck_count += count(convert(card['cards'][0]['code']))
            # player didn't bust, dealer hand played
            else:
                dealer_hand_count = 0
                #first card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                deck_count += count(convert(card['cards'][0]['code']))
                #second card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                deck_count += count(convert(card['cards'][0]['code']))
                print("Dealer Strength:", dealer_hand_count)
                # hit logic
                while dealer_hand_count < 16:
                    card = draw_card(deck_id, 1)
                    dealer_hand_count += convert(card['cards'][0]['code'])
                    deck_count += count(convert(card['cards'][0]['code']))
                    print("Dealer Strength:", dealer_hand_count)
                if ((dealer_hand_count > 21) or (player_hand_count > dealer_hand_count)):
                    print("Player Wins !\n\n")
                    money_to_bet += int(bet)
                    print("Current Wallet:", money_to_bet)
                elif(player_hand_count == dealer_hand_count):
                    print("Draw !\n\n")
                else:
                    print("Dealer Wins !\n\n")
                    money_to_bet -= int(bet)
                    print("Current Wallet:", money_to_bet)
        else: 
            exit()
        
def automated_play():
    print("Sorry, not implemented yet!")
    money_to_bet = input("Enter starting money:")
    while not money_to_bet.isdigit():
            print("\nPlease enter a number")
            money_to_bet = input("Enter starting money:")
    
    money_to_bet = int(money_to_bet)
    deck_id = generate_deck(1)
    deck_count = 0
    unit = 10
    won = 0
    lost = 0
    draw = 0
    while True:
        if(won+lost+draw != 0):
            print("Games Won %: ", (won)/(won+lost+draw))
            print("Games Lost %: ", (lost)/(won+lost+draw))
            print("Games Drawn %: ", (draw)/(won+lost+draw))
        print("Current Money: ", money_to_bet)
        game = 1
        games_to_play = input("Enter number of games to simulate or enter x to exit:")
        if games_to_play == 'x':
            exit()
        while not games_to_play.isdigit():
            games_to_play = input("Enter number of games to simulate or enter x to exit:")
        games_to_play = int(games_to_play)
        
        while game <= games_to_play :
            print(game)
            # set game bet
            bet = (deck_count-1)*unit
            if bet < unit:
                bet = unit

            # check deck size at start of round
            card = draw_card(deck_id, 1)
            if card['remaining'] <= 10:
                deck_count = reshuffle(deck_id)
            return_card(deck_id, card['cards'][0]['code'])   

            # running game count
            game += 1
            
            # player draw
            player_hand_count = 0
            # first card
            card = draw_card(deck_id, 1)
            player_hand_count += convert(card['cards'][0]['code'])
            deck_count += count(convert(card['cards'][0]['code']))
            # second card
            card = draw_card(deck_id, 1)
            player_hand_count += convert(card['cards'][0]['code'])
            deck_count += count(convert(card['cards'][0]['code']))

            # player hit loop
            while player_hand_count < 16:
                    card = draw_card(deck_id, 1)
                    player_hand_count += convert(card['cards'][0]['code'])
                    deck_count += count(convert(card['cards'][0]['code']))
            
            # condition when player bust, dealer hand still played
            if player_hand_count > 21:
                money_to_bet -= bet
                dealer_hand_count = 0
                #first card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                deck_count += count(convert(card['cards'][0]['code']))
                #second card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                deck_count += count(convert(card['cards'][0]['code']))
            # player didn't bust, dealer hand played
            else:
                dealer_hand_count = 0
                #first card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                deck_count += count(convert(card['cards'][0]['code']))
                #second card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                deck_count += count(convert(card['cards'][0]['code']))
                # hit logic
                while dealer_hand_count < 16:
                    card = draw_card(deck_id, 1)
                    dealer_hand_count += convert(card['cards'][0]['code'])
                    deck_count += count(convert(card['cards'][0]['code']))
                if ((dealer_hand_count > 21) or (player_hand_count > dealer_hand_count)):
                    won += 1
                    money_to_bet += bet
                elif(player_hand_count == dealer_hand_count):
                    draw += 1
                else:
                    lost += 1
                    money_to_bet -= bet

#event loop
while True:
    x = input("""
Enter 1 for manual play
Enter 2 for card automated play
Enter any key to exit\n
""")
    if x == "1":
        manual_play()
    if x == "2":
        automated_play()
    else:
        break