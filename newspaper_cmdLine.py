import argparse
from bs4 import BeautifulSoup
import requests
from datetime import date
# User can choose between several newspapers
# Washington Post, NY Times, LA Times etc
# Running the program will return an enumerated list
# of the n headlines from that day (default is 20, but the user can choose).
# The user can then decide whether they want to save the results to a text file
today = date.today()


# Users can select news stories by number and save to text file

def view(results):
    for num, dat in enumerate(results, 1):
        if len(dat.text.strip()) > 0:
                print(f'{num})...{dat.text.strip()}')

def scrape(newspaper: str, n = 20):
    urlDict = {"nyt": "https://www.nytimes.com/",
               "wapo": "https://www.washingtonpost.com/",
               "lat": "https://www.latimes.com/",
               "elp": "https://elpais.com/america/"} # abbrev : URL
    try:
        page = requests.get(urlDict[newspaper])
    except KeyError:
        print(f'Invalid key of {newspaper}')

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.findAll('h2')[:n]

    return results

def write(res, filename, newspaper):
    with open(filename, 'a') as o_file:
        o_file.write(f'Sourced from {newspaper}\n')
        o_file.write(f'{today}\n\n')
        for num, dat in enumerate(res, 1):
            if len(dat.text.strip()) > 0:
                o_file.write(f'{num})...{dat.text.strip()}\n')
        o_file.write('\n')
        print('Saved.')

def parse():
    # set up parser object
    newspapers = {'nyt': 'New York Times', 'wapo': 'Washington Post',
                'lat': 'Los Angeles Times', 'elp': 'El Pais'}

    parser = argparse.ArgumentParser()
    parser.add_argument('--save', action='store', required= False, help='Provide an optional file to which to append headlines.')

    # add option to append results to a text file._true
    group = parser.add_mutually_exclusive_group(required=True)
    # add mutually_exclusive_group choices

    group.add_argument("--nyt", action="store_true", help="View headlines from the New York Times")
    group.add_argument("--wapo", action="store_true", help="View headlines from the Washington Post")
    group.add_argument("--lat", action="store_true", help="View headlines from the Los Angeles Times") # Not working?
    group.add_argument("--elp", action="store_true", help="View headlines from El Pais")

    # parse the arguments
    # How many stories do you want to get?
    parser.add_argument("num",action="store",  nargs = '?', default=20, type=int, help="choose how many headlines you would like to see")

    args = parser.parse_args()
    selected = [(i, vars(args)[i]) for i in vars(args) if i in newspapers.keys() and vars(args)[i]][0]
    print(f'Sourcing from the {newspapers[selected[0]]}')
    print(today)

    # Select choice
    data = scrape(selected[0], args.num if args.num else 20)
    view(data)

    if args.save:
        print(f'...Saving to {args.save}...')
        write(data, args.save, newspapers[selected[0]])

parse()
