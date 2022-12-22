# This is a country connection game where you add a country and the computer will add a
# new country starting with the last Alphabet of the country you mentioned

from country_list import countries_for_language

countries = dict(countries_for_language('en'))
countries_of_world = []
for a, b in countries.items():
    countries_of_world.append(b.lower())

# print(country_of_world)
# print(len(country_of_world))

player_input = input("Name a country : ")
player_turn = True

connected_countries = []
found = True
while found:
    if player_turn:
        if player_input.lower() in connected_countries:
            print(f"Its a repeat")
            player_input = input(f"Name a country starting with {computer_country[-1]}")
        elif player_input.lower() in countries_of_world:
            connected_countries.append(player_input)
            last_character = player_input[-1]
            found = False
            for computer_country in countries_of_world:

                if found is True:
                    break
                elif computer_country not in connected_countries and computer_country[0] == last_character.lower():
                    print(f"My choice is {computer_country}")
                    connected_countries.append(computer_country)
                    player_input = input(f"Name a country starting with {computer_country[-1]} : ")
                    found = True
                    print(found)
                    #                    your_turn=False
                    break

            if found is False:
                print("I lost")

        else:
            print("Invalid country")
            print("Try again")
