import random

# Check if the user wants to stop the game
def checkStop(choice):
    if choice.lower() == "stop":
        print("You chose to stop, Game Over")
        exit()

# Displays the player's current health, tokens, inventory, and shield status
def showStatus(playerHealth, playerTokens, playerInventory, shieldTurnsLeft):
    print("\nHealth:", playerHealth)
    print("Tokens:", playerTokens)
    print("Inventory:")
    for item in playerInventory:
        print("-", item)
    if not playerInventory:
        print("- empty")
    if shieldTurnsLeft > 0:
        print("Shield active for", shieldTurnsLeft, "more turn(s).")

# Displays the game instructions
def showInstructions():
    print("\n--- Game Instructions ---")
    print("The game is an interactive story that asks you to make choices and that can change how the story plays out.")
    print("1. Your goal is to survive, fight monsters, and collect 25 tokens to buy the Victory Trophy.")
    print("2. You can fight monsters with your hands or a sword (if you have one).")
    print("3. Monsters deal different damage and drop different tokens:")
    print("   - Goblin: Deals 15 damage, drops 2 tokens")
    print("   - Troll: Deals 20 damage, drops 3 tokens")
    print("   - Dragon: Deals 30 damage, drops 5 tokens")
    print("4. The shop lets you buy useful items:")
    print("   - Health Potion (5 tokens) - Restores 20 health")
    print("   - Sword (10 tokens) - Helps defeat monsters but might break")
    print("   - Shield (8 tokens) - Protects you from all monster attacks for the next 2 turns, even if you don't encounter a monster.")
    print("   - Victory Trophy (25 tokens) - Buying this wins the game!")
    print("5. 70% chance to find a monster, 30% chance to find an item.")
    print("6. If your health reaches 0, you lose.")

# The shop allows the player to buy items using their tokens
def shop(playerTokens, playerInventory):
    print("\n--- Shop ---")
    print("1. Health Potion (5 tokens)")
    print("2. Sword (10 tokens)")
    print("3. Shield (8 tokens)")
    print("4. Victory Trophy (25 tokens) - Buying this wins the game!")
    print("5. Back")

    while True:
        choice = input("Enter the item number you want to buy or 5 to go back: ")
        checkStop(choice)

        if choice == "5":
            return playerTokens, playerInventory, False

        elif choice == "1" and playerTokens >= 5:
            playerInventory.append("Health Potion")
            playerTokens -= 5
            print("You bought a Health Potion!")

        elif choice == "2" and playerTokens >= 10:
            playerInventory.append("Sword")
            playerTokens -= 10
            print("You bought a Sword!")

        elif choice == "3" and playerTokens >= 8:
            playerInventory.append("Shield")
            playerTokens -= 8
            print("You bought a Shield!")

        elif choice == "4" and playerTokens >= 25:
            print("\nYou win the game!")
            return playerTokens - 25, playerInventory, True

        else:
            print("Not enough tokens or invalid choice.")

# The main function runs the game loop
def main():
    playerHealth = 100
    playerTokens = 0
    playerInventory = []
    shieldTurnsLeft = 0

    # List of monsters with their name, damage, hit chance, and token drop amount
    monsters = [
        ["Goblin", 15, 7, 2],
        ["Troll", 20, 6, 3],
        ["Dragon", 30, 4, 5]
    ]

    # The game continues as long as the player has health
    while playerHealth > 0:
        showStatus(playerHealth, playerTokens, playerInventory, shieldTurnsLeft)

        # Main menu options
        print("\n1. Check/Use inventory")
        print("2. Go to the shop")
        print("3. Continue Playing")
        print("4. Show Instructions")
        print("5. Stop")

        choice = input("Option: ")
        checkStop(choice)

        # Ends the game if the player chooses to stop
        if choice == "5":
            break

        # Manages the player's inventory
        elif choice == "1":
            while True:
                showStatus(playerHealth, playerTokens, playerInventory, shieldTurnsLeft)
                choice = input("Enter an item name to use it or type 'back' to exit the inventory: ").title()
                checkStop(choice)

                if choice == "Back":
                    break

                if choice in playerInventory:
                    if choice == "Health Potion": # Heals the player
                        playerHealth += 20
                        if playerHealth > 100:
                            playerHealth = 100 # Max health is 100
                        print("You used a Health Potion!")
                    elif choice == "Shield": # Activates shield
                        print("Shield activated! You will block attacks for the next 2 turns.")
                        shieldTurnsLeft = 2
                    playerInventory.remove(choice) # Removes the used item from the inventory
                else:
                    print("Invalid item.")

        # Opens the shop
        elif choice == "2":
            playerTokens, playerInventory, gameWon = shop(playerTokens, playerInventory)
            if gameWon:
                break # Ends the game if the player buys the Victory Trophy

        elif choice == "3": # Coninues the game
            probability = random.randint(1, 10)

            if probability <= 7: # 70% chance to encounter a monster
                monster = random.choice(monsters)
                monsterName, monsterDamage, monsterHitChance, monsterDropTokens = monster

                print("A " + monsterName + " appeared!")

                if shieldTurnsLeft > 0: # If the player has a shield active, block the attack
                    print("Your shield protected you and destroyed the", monsterName + "!")
                    print("The monster dropped", monsterDropTokens, "tokens!")
                    playerTokens += monsterDropTokens
                    shieldTurnsLeft -= 1
                    if shieldTurnsLeft == 0:
                        print("Your shield is no longer active.")
                    elif shieldTurnsLeft > 0:
                        print("Your shield is still active for", shieldTurnsLeft, "more turn(s).")
                # If the player doesn't have a shield active, fight normally
                else:
                    while True:
                        action = input("Do you want to fight with your hands (1) or use a sword (2)? ")
                        checkStop(action)

                        # Fight with hands
                        if action == "1":
                            fightChance = random.randint(1, 10)
                            if fightChance <= monsterHitChance:
                                print("The " + monsterName + " hit you and you lost " + str(monsterDamage) + " health!")
                                playerHealth -= monsterDamage
                                break
                            else:
                                print("You defeated the " + monsterName + "!")
                                print("The " + monsterName + " dropped " + str(monsterDropTokens) + " tokens!")
                                playerTokens += monsterDropTokens
                                break

                        # Fight with a sword
                        elif action == "2":
                            if "Sword" in playerInventory:
                                print("You defeated the " + monsterName + " using your sword!")
                                print("The " + monsterName + " dropped " + str(monsterDropTokens) + " tokens!")
                                if random.randint(1, 10) < 6:
                                    print("Sadly, your sword broke after the battle.")
                                    playerInventory.remove("Sword")
                                else:
                                    print("You still have your sword for future battles!")
                                playerTokens += monsterDropTokens
                                break
                            else:
                                print("You do not have a sword to use!")

        # Shows the instructions
        elif choice == "4":
            showInstructions()

        else:
            print("Invalid choice. Try again.")

    # Displays when player loses or stops.
    print("Game Over")

# Starts the game
main()
