#This is a country game where you say a country and the computer will say a new country starting with the last Alphabet of the country you mentioned

from country_list import available_languages
from country_list import countries_for_language


countries = dict(countries_for_language('en'))
country_of_world=[]
for a,b in countries.items():
   country_of_world.append(b.lower())

#print(country_of_world)
#print(len(country_of_world))

your_country=input("Name a country : ")
your_turn=True


current_country_list=[]
found=True
while found:
    if your_turn:
        if your_country.lower() in current_country_list:
            print(f"Its a repeat")
            your_country=input(f"Name a country starting with {country[-1]}")
        elif your_country.lower() in country_of_world:
            current_country_list.append(your_country)
            last_character=your_country[-1]
            found=False
            for country in country_of_world:

                if found is True:
                    break
                elif country not in current_country_list and country[0] == last_character.lower():
                    print(f"My choice is {country}")
                    current_country_list.append(country)
                    your_country=input(f"Name a country starting with {country[-1]} : ")
                    found=True
                    print(found)
#                    your_turn=False
                    break



            if found is False:
                print("I lost")

        else:
            print("Invalid country")
            print("Try again")
