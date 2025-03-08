import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Card values for Blackjack
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
    'J': 10, 'Q': 10, 'K': 10, 'A': 11  # Ace can be 1 or 11
}

def create_deck():
    """Returns a shuffled deck of 52 cards."""
    deck = [card for card in card_values.keys()] * 4  # 4 suits
    random.shuffle(deck)
    return deck

def hand_value(hand):
    """Calculates the best possible value of a hand (adjusting for Aces)."""
    value = sum(card_values[card] for card in hand)
    num_aces = hand.count('A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

# Store game results for visualization
results = {"Win": 0, "Loss": 0, "Draw": 0}
history = []

def play_interactive_blackjack():
    """Allows the user to play blackjack interactively and tracks results."""
    global results, history
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    
    # Player's turn
    while True:
        print(f"Your hand: {player_hand} (Value: {hand_value(player_hand)})")
        print(f"Dealer's visible card: {dealer_hand[0]}")
        if hand_value(player_hand) >= 21:
            break
        action = input("Do you want to (H)it or (S)tand? ").lower()
        if action == 'h':
            player_hand.append(deck.pop())
        elif action == 's':
            break
    
    # Dealer's turn
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    
    player_score = hand_value(player_hand)
    dealer_score = hand_value(dealer_hand)
    
    # Determine the winner
    print(f"Final hands:\nPlayer: {player_hand} (Value: {player_score})\nDealer: {dealer_hand} (Value: {dealer_score})")
    if player_score > 21:
        print("You busted! Dealer wins.")
        results["Loss"] += 1
    elif dealer_score > 21 or player_score > dealer_score:
        print("You win!")
        results["Win"] += 1
    elif player_score < dealer_score:
        print("Dealer wins!")
        results["Loss"] += 1
    else:
        print("It's a draw!")
        results["Draw"] += 1
    
    # Update history for visualization
    total_games = sum(results.values())
    history.append(results["Win"] / total_games * 100)
    plot_results()

def plot_results():
    """Plots the win rate over manually played games."""
    plt.figure(figsize=(10, 5))
    plt.plot(history, label="Win Rate (%)", color='g')
    plt.xlabel("Games Played")
    plt.ylabel("Win Rate (%)")
    plt.title("Blackjack Win Rate Over Time (Manual Games)")
    plt.legend()
    plt.grid()
    plt.show()

def run_simulation(n_rounds=100):
    """Simulates multiple rounds and plots win/loss trends."""
    sim_results = {"Win": 0, "Loss": 0, "Draw": 0}
    sim_history = []
    
    for _ in range(n_rounds):
        deck = create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        
        # Player's strategy: Stand at 17+
        while hand_value(player_hand) < 17:
            player_hand.append(deck.pop())
        
        # Dealer's turn
        while hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())
        
        player_score = hand_value(player_hand)
        dealer_score = hand_value(dealer_hand)
        
        # Determine outcome
        if player_score > 21:
            outcome = "Loss"
        elif dealer_score > 21 or player_score > dealer_score:
            outcome = "Win"
        elif player_score < dealer_score:
            outcome = "Loss"
        else:
            outcome = "Draw"
        
        sim_results[outcome] += 1
        sim_history.append(sim_results["Win"] / (sum(sim_results.values())) * 100)
    
    # Plot results
    plt.figure(figsize=(10, 5))
    plt.plot(sim_history, label="Win Rate (%)", color='g')
    plt.xlabel("Games Played")
    plt.ylabel("Win Rate (%)")
    plt.title("Blackjack Win Rate Over Time (Simulated Games)")
    plt.legend()
    plt.grid()
    plt.show()
    
    print("Final Results:")
    print(f"Wins: {sim_results['Win']} ({(sim_results['Win']/n_rounds)*100:.2f}%)")
    print(f"Losses: {sim_results['Loss']} ({(sim_results['Loss']/n_rounds)*100:.2f}%)")
    print(f"Draws: {sim_results['Draw']} ({(sim_results['Draw']/n_rounds)*100:.2f}%)")

# To play interactively and track results, call:
# play_interactive_blackjack()

# To run a simulation, call:
# run_simulation(1000)
