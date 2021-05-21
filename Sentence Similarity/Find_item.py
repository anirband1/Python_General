# check if item(key) in dict, if yes -> error cant be 2 items with same names

# DEPENDENCIES
import pandas as pd
import Sentence_comparision as sc

# from . import Sentence_comparision as sc


# displaying items which match most with the user input words
def return_items(similarity):
    max_len = 0
    for key in item_dict.keys():
        if len(key) > max_len:
            max_len = len(key)

    if similarity == 0:
        print('\n◊ There were no matches for your search ◊\n')
        return
    else:
        print("\nItems which are closest to your search:\n")
        for key, value in item_dict.items():
            if value == similarity > 0:
                print(f"• {key :{max_len + 2}}{similarity}%")
        print()
    return


def user_input():
    keywords = input("Describe your item (minimum 3 letters):   ")
    if keywords.isspace() or keywords == '' or len(keywords) < 3:
        print("\nInvalid. Sentence cannot be less than 3 letters\n")
        keywords = user_input()
    return keywords


# creating dataframe from excel sheet
path = "../../../../../../01-Documents/02-Microsoft/01-Excel/Items.xlsx"
data = pd.read_excel(path, engine='openpyxl')
df = pd.DataFrame(data)

# MAIN BODY

item_dict = {}
maximum = 0

keywords = user_input()

# iterates through each row in excel
# returns key(0, 1, 2 …) and tuple of row values ([(c1_r1, c2_r1), (c1_r2, c2_r2)])
for key, value in df.iterrows():

    item = value[0]
    description = value[1]

    # simulates out-of-stock objects
    # str(description) beacuse nan is a float
    if str(item) != 'nan' and str(description) != 'nan':

        # creates dictionary with item as key and similarity as value
        item_value = sc.compare(keywords, description)
        item_dict[item] = item_value
        maximum = max(maximum, item_value)

return_items(maximum)
