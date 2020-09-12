import random
import os
import os.path
from os import path

def shuffledDeck():  
    deck = ["2_♥","3_♥","4_♥","7_♥","8_♥","9_♥","10_♥","A_♥","2_♠","3_♠","4_♠","7_♠","8_♠","9_♠","10_♠","A_♠","2_♦","3_♦","4_♦","7_♦","8_♦","9_♦","10_♦","A_♦","2_♣","3_♣","4_♣","7_♣","8_♣","9_♣","10_♣","A_♣"] 
    random.shuffle(deck) 
    return deck 
    
def dealCard():
    y = shuffledDeck()
    x = random.choice(y) 
    return x
    
def total(hand, who):
    A = ["A_♠","A_♦","A_♣","A_♥"]
    sum_hand = 0
    for card in hand:
        if card in A:
            sum_hand += 11
        else:
            sum_hand += int(card[0])
    if (len(hand) == 2 and hand[0] in A and hand[1] in A) \
        or (len(hand) == 5 and sum_hand <= 21):
        return 21
    if len(hand) == 3 and hand[0][0]=="7" and hand[1][0]=="7" and hand[2][0]=="7":
        bank = 0
        if who == "player":
            money_player += bank   
        return 21
    return sum_hand
    
def compareHands(hand1,hand2):
    if hand2 > hand1:
        return -1
    return 1
    
def result(mom, player, bank, money_player):
    if compareHands(mom, player) == 1:
        print("You lose.")
        bank += bet
        money_player -= bet
    else:
        print("You win!")
        bank -= bet
        money_player += bet
        
def printBackup():
    file = open("backup.txt","a")
    if os.stat("backup.txt").st_size == 0:
        file.write("TURN"+"\t"+"BET"+"\t"+"PLAYER"+"\t"+"HOUSE"+"\t"+"WINNER"+"\t"+"BANK"+"\n")
    file.write(str(round_number)+"\t")
    file.write(str(bet)+"\t")
    file.write(str(total(player, "player"))+"\t")
    file.write(str(total(mom, "mom"))+"\t")
    if total(mom, "mom") <= 21 and total(player, "player") <= 21:
        if compareHands(mom, player) == 1:
            file.write("mom"+"\t")
        else:
            file.write("player"+"\t")
    elif total(mom, "mom") > 21 and total(player, "player") <= 21:
        file.write("player"+"\t")
    elif total(player, "player") > 21 and total(mom, "mom") <= 21:
        file.write("mom"+"\t")
    file.write(str(bank)+"\n")
    file.close()

round_number = 1
bank = 10
money_player = 10
last_game = False
 
if path.exists("backup.txt") != False:
    new_or_prev = input("Start new game (n) or continue previous game (c)?") 
    if new_or_prev == "n":
        f = open("backup.txt", "r+")
        f.truncate(0)
        f.close()
        round_number = 0
        bank = 10
        money_player = 0
        last_game = False
    else:
        f = open("backup.txt", "r")
        lines = f.read().splitlines()
        last_line = lines[-1]
        bank = int(last_line.rstrip("\n").split()[-1])
        f.close()
else:
    round_number = 0
    bank = 10
    money_player = 0
    last_game = False

while True:
    mom = []
    player = []
    move = "h"
    round_number += 1
    
    card = dealCard()
    player.append(card)
    print ("You got:" ,card)
    bet = int(input("Place your bet: "))
    while bet > bank:
        bet = int(input("Place your bet again: "))
    while move == "h":    
        card = dealCard()
        player.append(card)
        print ("You got:" ,card)   
        print("Your total now is:", total(player, "player"))
        if total(player, "player") == 21:
            print("You win!")
            bank -= bet
            money_player += bet
            break
        if total(player, "player") > 21:
            print("You lose.")
            bank += bet
            money_player -= bet
            break
        move = input("Hit (h) or stand (s)?")
    while total(player, "player") < 21 and total(mom, "mom")<17:
        card = dealCard()
        mom.append(card)
        print("House got:", card)
        print("House's total now is:", total(mom, "mom"))
    if total(mom, "mom") > 21:
        print("You win!")
        money_player += bet
        bank -= bet
    elif total(mom, "mom") == 21:
        print("You lose.")
        money_player -= bet
        bank += bet
    elif total(mom, "mom") < 21 and total(player, "player") < 21:
        result(mom, player, bank, money_player)
    if last_game == True:
        break
    if bank >= 30:
        last_game = True
    if bank == 0:
        result(mom, player, bank, money_player)
        break
               
    print("Bank's balance now is: ", bank)
    printBackup()
    game = ""
    while True:
        game = input("Continue(c), print history (h) or exit game (x)?")
        if game == "h":
            f = open("backup.txt", "r")
            for line in f:
                print(line)
            f.close()
        if game == "x":
            exit()
        if game == "c":
            break
            