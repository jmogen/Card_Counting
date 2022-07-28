import requests
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import sqlite3 as sql

def generate_deck(count):
    response = requests.post(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={count}")
    data = response.json()
    deckid = data['deck_id']
    return deckid

def draw_card(deckid, cards):
    response = requests.post(f"https://deckofcardsapi.com/api/deck/{deckid}/draw/?count={cards}")
    #response.raise_for_status()  # raises exception when not a 2xx response
    #print(response.status_code)
    try:
        data = response.json()
        return data
    except:
        draw_card(deckid, cards)
    # if response.status_code == 200:
        
    # else:
        

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
    money_to_bet = input("Enter starting money:")
    while not money_to_bet.isdigit():
            print("\nPlease enter a number")
            money_to_bet = input("Enter starting money:")
    
    money_to_bet = int(money_to_bet)
    deck_id = generate_deck(1)
    deck_count = 0
    unit = 10
    rounds = 1
    total_win = 0
    total_lost = 0
    total_draw= 0
    won = 0
    lost = 0
    draw = 0
    while True:
        games_to_play = input("Enter number of games to simulate or enter x to exit:")
        
        if games_to_play == 'x':
            break
        while not games_to_play.isdigit():
            games_to_play = input("Enter number of games to simulate or enter x to exit:")
        games_to_play = int(games_to_play)

        if(won+lost+draw != 0):
            print("Games Won %: ", (won)/(won+lost+draw))
            print("Games Lost %: ", (lost)/(won+lost+draw))
            print("Games Drawn %: ", (draw)/(won+lost+draw))

            data[f'Test {rounds}'] = win_results
            plt.plot(np.arange(data.shape[0]), data[f'Test {rounds}'], color='black', alpha=0.2)
            rounds += 1

        print(data)
        print("Current Money: ", money_to_bet)
        
        total_win += won
        total_lost += lost
        total_draw += draw
        
        # reset stats before new simulation
        won = 0
        lost = 0
        draw = 0
        game = 1
        win_results = []
        while game <= games_to_play:
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
            if(won+lost+draw != 0):
                win_results.append((won)/(won+lost+draw)-0.5)
            
            # running game count
            game += 1


# this was originally going to generate seperate tables based on the number of games played in the simulation
# I have realized it is likely less logic intensive if I simply use one large table and filter by number of rows when I plot the data later
def database_gen(games):
    games = 'Games_'+str(games)
    con = sql.connect('game_data_storage.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS " + f"{games} " + "(Simulation_1 text)")
    
    con.commit()
    cur.execute("SELECT * FROM " + f"{games}")
    items = cur.fetchall()
    print(items)
    con.close()
    print("Table Created")

def insert_entry(games, win_results):
    games = 'Games_'+str(games)
    con = sql.connect('game_data_storage.db')
    cur = con.cursor()
    items = cur.fetchall()
    print ('TEST', items)
    cursor = con.execute("SELECT * FROM " + f"{games}")
    names = list(map(lambda x: x[0], cursor.description))
    
    names = str(int(names[-1][-1])+1)
    if not items:
        names = '1'
    else:
        cur.execute("ALTER TABLE " + f"{games}" + " ADD COLUMN " + f'Simulation_{names}' + " text")
    print(names)
    for item in win_results:
        item = str(item)
        print("INSERT INTO " + f"{games} " + f'(Simulation_{names}) ' + "VALUES " + f"{item}")
        cur.execute("INSERT INTO " + f"{games} " + f'(Simulation_{names}) ' + "VALUES " + f"{item}")
    
    items = cur.fetchall()
    print(items)

    con.commit()
    con.close()

def graph_automated_play():
    money_to_bet = input("Enter starting money:")
    while not money_to_bet.isdigit():
            print("\nPlease enter a number")
            money_to_bet = input("Enter starting money:")
    
    money_to_bet = int(money_to_bet)
    deck_id = generate_deck(1)
    deck_count = 0
    unit = 10
    rounds = 1
    total_win = 0
    total_lost = 0
    total_draw= 0
    won = 0
    lost = 0
    draw = 0
    while True:
        simulation = 1
        games_to_play = input("Enter number of games to simulate or enter x to exit:")
        
        if games_to_play == 'x':
            break
        while not games_to_play.isdigit():
            games_to_play = input("Enter number of games to simulate or enter x to exit:")
        games_to_play = int(games_to_play)
        #database_gen(games_to_play)


        simulations = input("Enter number of times to repeat or enter x to exit:")
        
        if simulations == 'x':
            break

        while not simulations.isdigit():
            simulations = input("Enter number of times to repeat or enter x to exit:")
        simulations = int(simulations)

        
        while simulation <= simulations:
            #generate new deck for each sim
            #deck_id = generate_deck(1)
            print("Simulation", simulation)
            
            total_win += won
            total_lost += lost
            total_draw += draw
            
            # reset stats before new simulation
            won = 0
            lost = 0
            draw = 0
            game = 1
            win_results = []
            while game <= games_to_play:
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
                    lost += 1
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
                if(won+lost+draw != 0):
                    win_results.append((won)/(won+lost+draw)-0.5)
                    #print(win_results)
                
                # running game count
                game += 1
            simulation += 1
            #if(won+lost+draw != 0):
                #insert_entry(games_to_play, win_results)

            data[f'Test {rounds}'] = win_results
            plt.plot(np.arange(data.shape[0]), data[f'Test {rounds}'], color='black', alpha=0.2)
            rounds += 1

# initialize dataframe
data = pd.DataFrame()

def win_graph():
    plt.plot(np.arange(data.shape[0]), data.mean(axis=1), label='Average', color='red')
    plt.plot(np.arange(data.shape[0]), np.zeros(data.shape[0]), label='50 % Win Rate', color='blue')
    plt.title("Win Percentage Analysis")
    plt.xlabel("Games Played")
    plt.ylabel("Win Percentage")
    plt.legend()
    plt.savefig('2000 Game Win Analysis')
    plt.show()

#event loop
def main():
    while True:
        x = input("""
Enter 1 for manual play
Enter 2 for automated play
Enter 3 for graph generation
Enter any key to exit\n
""")
        if x == "1":
            manual_play()
        if x == "2":
            automated_play()
        if x == "3":
            graph_automated_play()
            win_graph()
        else:
            break

if __name__ == "__main__":
    main()