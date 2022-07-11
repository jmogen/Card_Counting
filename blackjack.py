from sre_constants import JUMP
from turtle import goto
import requests


def generate_deck(count):
    response = requests.post(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={count}")
    data = response.json()
    deckid = data['deck_id']
    return deckid

def draw_card(deckid, cards):
    response = requests.post(f"https://deckofcardsapi.com/api/deck/{deckid}/draw/?count={cards}")
    data = response.json()
    # if data['remaining'] <= 10:
    #     reshuffle(deckid)
    # print('SECOND', response.content, '\n')
    # print(data['cards'][0]['code'])
    return data

def reshuffle(deckid):
    requests.post(f"https://deckofcardsapi.com/api/deck/{deckid}/shuffle")
    return None

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

#d31xyjxoan40

def manual_play():
    money_to_bet = input("Enter starting money:")
    while not money_to_bet.isdigit():
            print("\nPlease enter a number")
            money_to_bet = input("Enter starting money:")
    money_to_bet = int(money_to_bet)
    deck_id = generate_deck(1)
    game = 1
    while True:
        print(f"Game: {game}")
        game += 1
        bet = input("Enter Bet:")
        while not bet.isdigit():
            print("\nPlease enter a number")
            bet = input("Enter Bet:")
        print("\nEnter 1 to draw")
        print("Enter any key to exit\n")
        x = input()
        if x == "1":
            player_hand_count = 0
            #first card
            card = draw_card(deck_id, 1)
            player_hand_count += convert(card['cards'][0]['code'])
            #second card
            card = draw_card(deck_id, 1)
            player_hand_count += convert(card['cards'][0]['code'])

            while True:
                print(f"Hand Strength: {player_hand_count}")
                print("Enter 1 to hit")
                print("Enter any key to stay\n")
                if input() == "1":
                    card = draw_card(deck_id, 1)
                    player_hand_count += convert(card['cards'][0]['code'])
                    
                else:
                    break 
            if player_hand_count > 21:
                print("Dealer Wins !\n\n")
                money_to_bet -= int(bet)
                print("Current Wallet:", money_to_bet)
                dealer_hand_count = 0
                #first card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                #second card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
            else:
                dealer_hand_count = 0
                #first card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                #second card
                card = draw_card(deck_id, 1)
                dealer_hand_count += convert(card['cards'][0]['code'])
                print("Dealer Strength:", dealer_hand_count)
                while dealer_hand_count < 16:
                    card = draw_card(deck_id, 1)
                    dealer_hand_count += convert(card['cards'][0]['code'])
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
    return None

#event loop
while True:
    print("Enter 1 for manual play")
    print("Enter 2 for card automated play")
    print("Enter any key to exit\n")
    if input() == "1":
        manual_play()
    elif input() == "2":
        automated_play()
    else:
        break