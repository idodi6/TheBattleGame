from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random
# Create Black Magic
fire = Spell('Fire', 25, 600, 'black')
thunder = Spell('Thunder', 25, 600, 'black')
blizzard = Spell('Blizzard', 25, 600, 'black')
meteor = Spell('Meteor', 40, 1200, 'black')
quake = Spell('Quake', 14, 140, 'black')

# Create White Magic
cure = Spell('Cure', 25, 620, 'white')
cura = Spell('Cura', 32, 1500, 'White')

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("Mega Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Generate list of spells and items for players :

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5}, {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 5}, {"item": hielixir, "quantity": 2},
                {"item": grenade, "quantity": 5}]

enemy_spells = [fire, meteor, cure]

# Instantiate People
player1 = Person('Guy:  ', 3260, 132, 300, 34, player_spells, player_items)
player2 = Person('John: ', 4160, 188, 311, 34, player_spells, player_items)
player3 = Person('Mike: ', 3089, 174, 288, 34, player_spells, player_items)

enemy2 = Person("Magus: ", 1250, 130, 560, 325, enemy_spells, [])
enemy1 = Person('Darth: ', 12000, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp:   ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("==================")
    print('\n\n')
    print("NAME                 HP                          MP")
    for player in players:
        player.get_stats()

    print('\n')
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        print(player.choose_action())
        choice = input("Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose Magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + '\n' + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == 'black':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose Item: ")) - 1

            if item_choice == -1:
                continue
            item = player.items[item_choice]["item"]

            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == 'elixir':
                if item.name == 'Mega Elixir':
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "Fully restores HP/MP" + bcolors.ENDC)
            elif item.type == 'attack':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to "
                      + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # Check if battle is over

    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
    # Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False
    # Check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your Enemy has defeated you!" + bcolors.ENDC)
        running = False

    # Enemy attack Phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)
        if enemy_choice == 0:
            # Chose Attack
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", ""), "Enemy attacks " + players[target].name.replace(" ", "") + "for",
                  enemy_dmg)
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            print("Enemy Chose", spell, "damage is", magic_dmg)
