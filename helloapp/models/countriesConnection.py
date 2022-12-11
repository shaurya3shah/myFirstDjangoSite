import random
from enum import Enum

from country_list import countries_for_language


class CountriesConnection:
    score = 0
    connected_countries = []
    player_countries = []
    computer_countries = []
    countries_of_world = []
    last_player_country = str
    last_computer_country = str
    countries_connection = ''

    def connect_country(self, player_input):
        player_input = player_input.lower()
        print(f"player_input: " + player_input)
        # print(f"countries_of_world: " + self.countries_of_world.__str__())

        if player_input.lower() in self.connected_countries:
            print(f"Its a repeat")
            return Result.REPEAT
        elif self.last_computer_country and player_input[0].lower() != self.last_computer_country[-1]:
            print(f"Cannot connect")
            return Result.DISCONNECT
        elif player_input.lower() in self.countries_of_world:
            self.add_player_country(player_input)
            last_character = player_input[-1]
            found = False
            random.shuffle(self.countries_of_world)
            for computer_country in self.countries_of_world:
                if computer_country not in self.connected_countries and computer_country[0] == last_character.lower():
                    print(f"Computer choice is {computer_country}")
                    self.add_computer_country(computer_country)
                    found = True
                    print(found)
                    return Result.CONNECTED

            if found is False:
                print("Coumpter exhausted the list of countries")
                return Result.EXHAUSTED
        else:
            return Result.INVALID

    def add_player_country(self, player_input):
        self.connected_countries.append(player_input)
        self.last_player_country = player_input
        self.player_countries.append(player_input)

        if not self.countries_connection:
            self.countries_connection = '<span style="color: green; ">' + player_input + '<span>'
        else:
            self.countries_connection = self.countries_connection + ' --> ' + '<span style="color: green; ">' + player_input + '<span>'

        self.score += 1

    def add_computer_country(self, computer_country):
        self.connected_countries.append(computer_country)
        self.last_computer_country = computer_country
        self.computer_countries.append(computer_country)
        self.countries_connection = self.countries_connection + ' --> ' + '<span style="color: blue; ">' + computer_country + '<span>'
        self.score += 1

    def __init__(self):
        print("initiating countries connection")
        if not self.countries_of_world:
            countries = dict(countries_for_language('en'))
            for a, b in countries.items():
                self.countries_of_world.append(b.lower())

        random.shuffle(self.countries_of_world)

        self.score = 0
        self.connected_countries = []
        self.player_countries = []
        self.computer_countries = []
        self.last_player_country = ''
        self.last_computer_country = ''
        self.countries_connection = ''


class Result(Enum):
    REPEAT = 1
    CONNECTED = 2
    INVALID = 3
    EXHAUSTED = 4
    DISCONNECT = 5

    def __str__(self):
        return self.name
