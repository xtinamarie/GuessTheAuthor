"""
==============================
    Web Scraping Project
==============================
This project was orginally placed in one of my other repositories: https://github.com/kristinalagasca/Modern-Python3-Bootcamp/blob/main/WebScraping/P4WebScraping.py

I placed this project separately from that repository to make it easier to find.

In this project the user will be building a quotes guessing game. When run, your program will scrape a website for
a collection of quotes. Pick one at random and display it. The player will have four chances to guess who said the
quote. After every wrong guess they'll get a hint about the author's identity.
"""

import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice as c



BASE_URL = "http://quotes.toscrape.com"


def scrape_quotes():
    all_quotes = []
    url = "/page/1"
    while url:
        res = requests.get(f"{BASE_URL}{url}")
        print(f"Now scraping {BASE_URL}{url} ...")
        soup = BeautifulSoup(res.text)
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": quote.find("a")["href"]
            })

        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        # sleep(2)

    return all_quotes


def start_game(all_quotes):
    quote = c(all_quotes)
    remaining_guesses = 4
    print("Here's a quote: ")
    print(quote["text"])
    guess = ''
    while guess.lower != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining {remaining_guesses}: ")
        if guess.lower() == quote["author"].lower():
            print("YOU GOT IT!! :D")
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{BASE_URL}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(f"Here's a hint: The author was born on {birth_date} and {birth_place}.")
            if guess.lower() == quote["author"].lower():
                print("YOU GOT IT!! :D")
                break
        elif remaining_guesses == 2:
            print(f"Here's a hint. Author's first name starts with: {quote['author'][0]}")
            if guess.lower() == quote["author"].lower():
                print("YOU GOT IT!! :D")
                break
        elif remaining_guesses == 1:
            last_initial = quote['author'].split(" ")[1][0]
            print(f"Here's a hint. Author's last name starts with: {last_initial}")
            if guess.lower() == quote["author"].lower():
                print("YOU GOT IT!! :D")
                break
        else:
            print(f"Sorry you ran out of guesses. The answer was {quote['author']}")

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n)? ")
    if again.lower() in ('yes', 'y'):
        return start_game(all_quotes)
    else:
        print("Thanks for playing! See you next time.")

quotes = scrape_quotes()
start_game(quotes)