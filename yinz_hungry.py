import sys
import requests
import json
import webbrowser
from urllib.request import urlopen
import pandas as pd

api_key = 'Zr06BpRhoUByAHpcsEm9qm3eETk9rRNPCGPxKqD2_XMDvpLLBF_fdn681G2ND015-_3RWCYb6LDXRmPe5Zz0hJkBblCz2yJ76sL7B7eSdpN-IExrUGfAhm88ff1SXnYx'
headers = {'Authorization' : 'Bearer {}'.format(api_key)}

restaurantDF = pd.read_csv('restData.csv')


# REMOVE THE '.0' FROM THE ADDRESS STRINGS
def zipstrip(z):
    z = z.strip('0')
    z = z.strip('.')
    return z

# REMOVE THE NANs FROM ADDRESS
def nanstrip(z):
    z = z.strip('nan')
    return z

# Following code applies to both frySearch and healthInfo functions

# DOWNLOAD THE CSV FILE FROM THE WEB
url = 'https://data.wprdc.org/datastore/dump/410f80a1-d18c-44f3-9964-2205b2ea7f5a'
download = urlopen(url)

# IMPORT THE CSV INTO A PANDAS DATAFRAME
global inspections 
inspections = pd.read_csv(download)

# SELECTING RELEVANT COLUMNS
inspections = inspections[['placard_st',
                       'placard_desc',
                       'facility_name',
                       'description',
                       'num',
                       'street',
                       'city',
                       'state',
                       'zip',
                       'inspect_dt']]

# DROP THE ROWS WITH IRRELEVANT DATA
# descriptions column: only restaurants with liquor and restaurants without liquor
# alternatively pick category codes of 201 and 211
inspections = inspections[inspections.description != 'Adult Food Service']
inspections = inspections[inspections.description != 'Bakery']
inspections = inspections[inspections.description != 'Banquet Hall']
inspections = inspections[inspections.description != 'Caterer']
inspections = inspections[inspections.description != 'Chain Bakery']
inspections = inspections[inspections.description != 'Chain Packaged Food Only']
inspections = inspections[inspections.description != 'Chain Retail/Convenience Store']
inspections = inspections[inspections.description != 'Chain Supermarket']
inspections = inspections[inspections.description != 'Child Food Service']
inspections = inspections[inspections.description != 'Church Kitchen']
inspections = inspections[inspections.description != 'Commissary']
inspections = inspections[inspections.description != 'Community Service Facilities']
inspections = inspections[inspections.description != 'Concession Stands']
inspections = inspections[inspections.description != 'Firehall without Liquor']
inspections = inspections[inspections.description != 'Firehall with Liquor']
inspections = inspections[inspections.description != 'Food Banks/ Food Pantries']
inspections = inspections[inspections.description != 'Food Processor']
inspections = inspections[inspections.description != 'Hospital, Gov, University (limited)']
inspections = inspections[inspections.description != 'Hospital/Other Institution']
inspections = inspections[inspections.description != 'Hotels - Limited Menu Food Service']
inspections = inspections[inspections.description != 'Mobile - Tier II ( Prepared Foods)']
inspections = inspections[inspections.description != 'Mobile Ã¢Â€Â“ Tier I (Unopened Pre-packaged Food Only)']
inspections = inspections[inspections.description != 'Nursing Home']
inspections = inspections[inspections.description != 'Nursing Home/Fee Exempt']
inspections = inspections[inspections.description != 'Nursing Home/Personal Care Comb.']
inspections = inspections[inspections.description != 'Nursing Home/Personal Care Comb./Fee Exempt']
inspections = inspections[inspections.description != 'Nursing Home/Personal Care Snack Bar']
inspections = inspections[inspections.description != 'Nursing Home/Personal Care Snack Bar/Fee Exempt']
inspections = inspections[inspections.description != 'Packaged Food Only']
inspections = inspections[inspections.description != 'Personal Care Boarding Home']
inspections = inspections[inspections.description != 'Personal Care Boarding Home/Fee Exempt']
inspections = inspections[inspections.description != 'Pool Snack Bar/No Liquor']
inspections = inspections[inspections.description != 'Pool Snack Bar/With Liquor']
inspections = inspections[inspections.description != 'Refridgerated Warehouse']
inspections = inspections[inspections.description != 'Retail/Convenience Store']
inspections = inspections[inspections.description != 'Rooming House with Guest food Service']
inspections = inspections[inspections.description != 'School Full Service Kitchen']
inspections = inspections[inspections.description != 'School Headstart']
inspections = inspections[inspections.description != 'School Satellite Kitchen']
inspections = inspections[inspections.description != 'School Snack Bar']
inspections = inspections[inspections.description != 'Seasonal/Pool Snack Bar']
inspections = inspections[inspections.description != 'Social Club-Bar Only']
inspections = inspections[inspections.description != 'Supermarket']
inspections = inspections[inspections.description != 'Traditional Boarding Home']
inspections = inspections[inspections.description != 'Traditional Boarding Home/Fee Exempt']
inspections = inspections[inspections.description != 'Transient Caterer']
inspections = inspections[inspections.description != 'Transient Retail Food Processor']
inspections = inspections[inspections.description != 'University Food Service']
inspections = inspections[inspections.description != 'Warehouse']

# RENAME THE COLUMNS
inspections.columns = ['INSPECTION DESCRIPTION',
                   'INSPECTION RESULT',
                   'NAME',
                   'CATEGORY',
                   'NUMBER',
                   'STREET',
                   'CITY',
                   'STATE',
                   'ZIP',
                   'INSPECTION DATE']

# CONCATINATE THE ADDRESS COLUMNS INTO ONE
inspections['ADDRESS'] = inspections['NUMBER'].map(str) + ' ' + inspections['STREET'].map(str) + ' ' + inspections[
'CITY'].map(str) + ' ' + inspections['STATE'].map(str) + ' ' + inspections['ZIP'].map(str)


# ------------- Start Menu

def startMenu():
    print()
    print('YINZ Hungry?')
    print()
    print('1. Feed Me')
    print('2. No, Leave me Alone')
    print('3. I need fries now')
    print()
    startChoice = input('Enter your choice (1-3): ')
    try:
        startChoice = int(startChoice)
    except ValueError:
        print("Not a valid choice.")
        sys.exit()

    if startChoice < 1 or startChoice > 3:
        print("Not a valid choice.")
        startChoice = 2 # Quit if the user is stupid

    return startChoice

# ------------- Fry Search

def frySearch():
    # DOWNLOAD THE CSV FILE FROM THE WEB

    inspections['ADDRESS'] = inspections['ADDRESS'].apply(zipstrip)

    inspections['ADDRESS'] = inspections['ADDRESS'].apply(nanstrip)

    # PRIMANTIS
    primantis = inspections[['NAME', 'ADDRESS']]
    primantis = primantis.sort_values('NAME')
    primantis = primantis.drop_duplicates()
    primantis['PINDEX'] = [i for i in range(len(primantis))]
    primantis = primantis.set_index('PINDEX')

    primantisNames = ['Heinz Field / Primanti Brothers Rm#110',
                      'Heinz Field / Primanti Brothers Rm#132',
                      'PNC Park / 02.47.01Primanti Brothers #110',
                      'Primanti Bros - The Waterfront',
                      'Primanti Bros Bar & Restaurant',
                      'Primanti Bros Food Trailer (PT-853B9) MFF4',
                      'Primanti Bros Moon Twp',
                      'Primanti Bros Restaurant',
                      'Primanti Bros Restaurant & Bar',
                      'Primanti Bros Resturant',
                      'Primanti Bros. - Allison Park',
                      'Primanti Brothers',
                      'Primanti Brothers Bar & Grill',
                      'Primanti Brothers Restaurant']

    primantiBros = pd.DataFrame(columns=('NAME', 'ADDRESS'))

    for primanti in primantisNames:
        pb = primantis[primantis['NAME'] == primanti]
        primantiBros = primantiBros.append(pb)

    # RE-ORDER THE COLUMNS
    primantiBros = primantiBros.reindex(columns=['NAME', 'ADDRESS'])
    primantiBros.reset_index(drop=True, inplace=True)

    # RETURN RESULTS
    print()
    print("Enjoy Your Fries!")
    print(primantiBros)
    print()

# ------------- Cuisine Menu

def cuisineMenu():
    print()
    print('What are you in the mood for?')

    # We are subsetting here since each cuisine type should only be listed once
    cuisines = restaurantDF['Cuisine'].copy()
    cuisines = cuisines.drop_duplicates()
    cuisines = cuisines.reset_index()
    # to_string makes printing more pretty
    print(cuisines['Cuisine'].to_string())

    quitOp = len(cuisines)
    print(str(quitOp) + '{:>20}'.format('Quit'))

    print()
    choiceB = input('Enter your choice (0-{}): '.format(len(cuisines)))
    print()
    try:
        choiceB = int(choiceB)
    except ValueError:
        print("Not a valid choice.")
        sys.exit()

    if choiceB < 0 or choiceB > len(cuisines):
        print("Not a valid choice.")
        sys.exit()
    elif choiceB == len(cuisines):
        print("Quitting...")
        sys.exit()
    elif str(choiceB).isdigit() == False:
        print("Not a valid choice.")
        sys.exit()

    return choiceB

# ------------- Restaurant Menu

def restaurantMenu(cuisineMenuChoice):
    print()
    print('Where would you like to eat?')
    counter = 0

    # Subsetting again for same reasons. Will reconcile at end of func.
    cuisines = restaurantDF['Cuisine'].copy()
    cuisines = cuisines.drop_duplicates()
    cuisines = cuisines.reset_index()
    cuisines = cuisines.drop(columns=['index'])

    # Name of the cuisine previously chosen
    cuisine_type = cuisines.loc[cuisineMenuChoice]
    print()
    print(cuisine_type['Cuisine'], "CUISINE")

    # Boolean to see if a row's cuisine type is the one a user selected. Filter on the boolean
    is_cuisine = restaurantDF['Cuisine'] == cuisine_type['Cuisine']
    filteredByCusine = restaurantDF[is_cuisine]

    print()

    names = []

    # Loop through filtered restaurants and give their name, Twice Rated, and description
    for index, row in filteredByCusine.iterrows():
        print(str(counter) + ':\nName:', row['Name'])
        print('On Both "Best of" Lists?', row['Twice Rated'])
        print("Restaurant Description:", row['Description'])
        counter = counter + 1
        names.append(row['Name'])
        print()
    quitOp = counter
    print(str(quitOp) + ': Quit')

    print()
    choiceC = input('Enter your choice (0-{}): '.format(len(filteredByCusine)))
    print()
    try:
        choiceC = int(choiceC)
    except ValueError:
        print("Not a valid choice.")
        sys.exit()

    if choiceC < 0 or choiceC > len(filteredByCusine):
        print("Not a valid choice.")
        sys.exit()
    elif choiceC == len(filteredByCusine):
        print("Quitting...")
        sys.exit()
    elif str(choiceC).isdigit() == False:
        print("Not a valid choice.")
        sys.exit()

    # This basically re-synchs the user's choice to the proper index in restaurantDF since we had previously filtered
    choiceC = int(restaurantDF[restaurantDF['Name'] == names[choiceC]].index.values)

    return choiceC

# ------------- Restaurant Info Menu

def restInfoMenu(restaurantMenuChoice):
    print()
    print('What would you like to learn about {}?'.format(restaurantDF['Name'][restaurantMenuChoice]))

    menOps = ["1. Phone Number & Address", "2. Directions to {}".format(restaurantDF['Name'][restaurantMenuChoice])
        , "3. Yelp Review Excerpts for {}".format(restaurantDF['Name'][restaurantMenuChoice])
        , "4. Health Inspection Information"
        , "5. Quit"]

    for op in menOps:
        print(op)

    print()
    choiceD = input('Enter your choice (1-5): ')
    print()
    try:
        choiceD = int(choiceD)
    except ValueError:
        print("Not a valid choice.")
        sys.exit()

    if choiceD < 0 or choiceD > 5:
        print("Not a valid choice.")
        sys.exit()
    elif choiceD == 5:
        print("Quitting...")
        sys.exit()
    elif str(choiceD).isdigit() == False:
        print("Not a valid choice.")
        sys.exit()

    return choiceD

# ------------- Phone Address

def phoneAddress(restaurantMenuChoice, jsonInfo):
    print()
    print('{:30} {:15} {:15}'.format("Name", "Phone Number", "Address"))
    print('{:30} {:<15} {:15}'.format(restaurantDF['Name'][restaurantMenuChoice]
                                     , restaurantDF['Phone Number'][restaurantMenuChoice]
                                     , jsonInfo["businesses"][0]['location']['address1'] + ' ' +
                                     jsonInfo["businesses"][0]['location']['city']))
    print()

# -------------Phone search

def phoneSearch(restName):
    url = 'https://api.yelp.com/v3/businesses/search/phone'
    # Get phone number from restaurantDF
    phoneNum = restaurantDF.at[restName, 'Phone Number']
    # When served a phone number, we need this to use in our API request
    params = {'phone': '+1{}'.format(phoneNum)}

    # Our phone search API request
    req = requests.get(url, params=params, headers=headers)
    # Store what we get in a variable
    parsed = json.loads(req.text)

    return parsed

# -----------map stuff

# I promise I need this
def remove(string):
    return string.replace(" ", "")

def getDirections(phoneSearchReturn):

    or_city = str(input("Enter Your Origin City: "))
    or_add = str(input("Enter Your Origin Street Address: "))

    # Grab the street address and city from the phone search
    dest_add = phoneSearchReturn["businesses"][0]['location']['address1']
    #Probably unnecessary dest_add = remove(dest_add)
    dest_city = phoneSearchReturn["businesses"][0]['location']['city']

    # Use the Google Maps URL API to create a link that will take you from source to destination
    mapurl = 'https://www.google.com/maps/dir/?api=1&origin={}+{}&destination={}+{}&travelmode=driving'\
        .format(or_add, or_city, dest_add,dest_city)

    # Auto open the returned URL
    webbrowser.open_new_tab(mapurl)

# ---------------Reviews
def yelpReview(phoneSearchReturn):
    # Grab the id of the parsed restaurant
    id = phoneSearchReturn["businesses"][0]['id']

    # get the URL for the reviews api call
    revurl = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(id)

    # make the reviews api call
    revreq = requests.get(revurl, headers=headers)

    # store it
    revParsed = json.loads(revreq.text)

    # loop through the three given reviews and print them nicely
    reviews = revParsed['reviews']

    print()

    for review in reviews:
        print("Reviewer:", review['user']['name'])
        print("Rating:", review['rating'])
        print(review['text'])
        print()
    
    print()

# ------------------------ Health Inspection Display

def healthInfo(restaurantMenuChoice, inspections= inspections):

    print()
    # REMOVE THE '.0' FROM THE ADDRESS STRINGS
    inspections['ADDRESS'] = inspections['ADDRESS'].apply(zipstrip)

    # DROP OLD ADDRESS COLUMNS AND THE DESCRIPTION COLUMN
    inspections = inspections[['INSPECTION RESULT',
                               'NAME',
                               'ADDRESS',
                               'INSPECTION DATE']]

    # RE-ORDER THE COLUMNS
    inspections = inspections.reindex(columns=['NAME',
                                               'INSPECTION RESULT',
                                               'INSPECTION DATE',
                                               'ADDRESS'])

    # REMOVE THE BAD CHARACTERS
    def badChar(name):
        name = name.replace('^\w', '')
        name = name.replace('\'', '')
        return name

    inspections['NAME'] = inspections['NAME'].apply(badChar)

    # CHANGE THE RESTAURANT NAMES TO MATCH INSPECTION NAMES
    def rename(name):
        if name == 'B52':
            name = 'B52 CAFE'
        elif name == 'BAR MARCO @ THE FIREHOUSE':
            name = 'BAR MARCO'
        elif name == 'Fairmont PGH / fl.2 Restaurant / Andy\'s':
            name = 'FL. 2'
        elif name == 'Hyeholde Restaurant':
            name = 'HYEHOLDE'
        elif name == 'Legume Bistro / Butterjoint':
            name = 'LEGUME'
        elif name == 'or, The Whale / Distrikt Hotel':
            name = 'OR, THE WHALE'
        elif name == 'Spoon / BRGR':
            name = 'SPOON'
        elif name == 'Cafe 33 Taiwanese Bistro':
            name = 'TAIWANESE BISTRO CAFE 33'
        elif name == 'Tessaro\'s':
            name = 'TESSAROS AMERICAN BAR & HARDWOOD GRILL'
        elif name == 'Carnegie Museum / Cafe Carnegie':
            name = 'THE CAFE CARNEGIE'
        elif name == 'Soba Lounge / UMI':
            name = 'UMI JAPANESE RESTAURANT'
        elif name == 'Ace Hotel Pittsburgh / Whitfield Restaurant':
            name = 'WHITFIELD'
        elif name == 'Poulet Bleu':
            name = 'POULET BLEU'
        elif name == 'Bitter Ends Garden & Lucheonette':
            name = 'BITTER ENDS GARDEN & LUNCHEONETTE'
        elif name == 'Cocothe\'':
            name = 'COCOTHE'
        elif name == 'Udipi':
            name = 'UDIPI CAFE'
        return name

    inspections['NAME'] = inspections['NAME'].apply(rename)

    # RESTAURANT NAMES THAT DON'T HAVE HEALTH INSPECTION DATA
    # 'ELEVEN CONTEMPORARY KITCHEN'
    # 'LAUTREC' <-- DONT HAVE

    # MAKE THE RESTAURANT NAME THE INDEX
    inspections['NAME'] = inspections['NAME'].apply(lambda x: x.upper())
    inspections = inspections.set_index('NAME')

    # PULL HEALTH INSPECTION DATA FOR RESTAURANT CHOICE
    try:
        print(inspections.loc[restaurantDF['Name'][restaurantMenuChoice]].to_string())
    except:
        print('Erroneous Health Inspection Data')
    print()

# ------------------------ Main

def main():

    startChoice = startMenu()

    while startChoice != 2:
        if startChoice == 1:
            cuisineMenuChoice = cuisineMenu()

            restaurantMenuChoice = restaurantMenu(cuisineMenuChoice)

            jsonInfo = phoneSearch(restaurantMenuChoice)

            restInfoMenuChoice = restInfoMenu(restaurantMenuChoice)

            while restInfoMenuChoice != 5:
                if restInfoMenuChoice == 1:
                    phoneAddress(restaurantMenuChoice, jsonInfo)
                elif restInfoMenuChoice == 2:
                    getDirections(jsonInfo)
                elif restInfoMenuChoice == 3:
                    yelpReview(jsonInfo)
                elif restInfoMenuChoice == 4:
                    healthInfo(restaurantMenuChoice)

                else:
                    print("Quiting...")
                    sys.exit()
                restInfoMenuChoice = restInfoMenu(restaurantMenuChoice)

        elif startChoice == 3:
            frySearch()
            break

if __name__ == '__main__':
    main()
