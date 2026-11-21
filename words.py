"""
    Authors: Aiden Grey

    Email: amgrey70@gmail.com

    Program: words.py

    Purpose: janky wordplay

"""
import time
from collections import Counter
from pathlib import Path

# Finds the exact folder where the program file is saved
script_dir = Path(__file__).parent
file_path = script_dir / "words.txt"

with open(file_path, 'r') as words:
    words_list = [line.strip() for line in words]
# words_list is a list containing every word in the english language in alphabetical order

start_time = time.perf_counter()

def ask_yes_no(prompt):
    choice = input(f"{prompt} (y/n): ").upper()
    while choice not in ('Y', 'N'):
        print("Invalid option.")
        choice = input(f"{prompt} (y/n): ").upper()
    return choice == 'Y'

print()
print("This program accesses a massive list containing effectively every word in the english language.")
print("It contains proper nouns, prefixes, abbreviations, hyphenated compound words, and some numbers.")
print()
want_to_modify = ask_yes_no("Would you like to modify this list?")

if want_to_modify:
    nonos_as_in_number_of_nos_because_n_with_superscript_o_means_that_you_know_what_never_mind_forget_it = 0
    remove_symbols = ask_yes_no("Remove entries including characters other than letters or digits?")
    if remove_symbols:
        words_list = [word for word in words_list if word.isalnum()]
        remove_numbers = ask_yes_no("Remove entries with digits?")
        if remove_numbers:
            words_list = [word for word in words_list if word.isalpha()]
    else:
        remove_hyphens = ask_yes_no("Remove hyphenated entries?")
        if remove_hyphens:
            words_list = [word for word in words_list if not "-" in word]
        else:
            nonos_as_in_number_of_nos_because_n_with_superscript_o_means_that_you_know_what_never_mind_forget_it += 2

    remove_capitals = ask_yes_no("Remove entries with capital letters? NOTE: Removing words containing capital letters can have unintended consequences.\nFor example, 'Scrabble' is a proper noun, and 'scrabble' is a verb, but only the former is in words.txt. Proceed?")
    if remove_capitals:
        words_list = [word for word in words_list if word.islower()]
    else:
        remove_title_case = ask_yes_no("Remove title-cased entries?")
        if remove_title_case:
            words_list = [word for word in words_list if not word[0].isupper()]
        else:
            nonos_as_in_number_of_nos_because_n_with_superscript_o_means_that_you_know_what_never_mind_forget_it += 2

    remove_without_vowels = ask_yes_no("Remove entries lacking vowels?")
    if remove_without_vowels:
        vowels = {"A", "E", "I", "O", "U", "Y"}
        words_list = [word for word in words_list if not vowels.isdisjoint(word.upper())]
    else:
        nonos_as_in_number_of_nos_because_n_with_superscript_o_means_that_you_know_what_never_mind_forget_it += 1

    if nonos_as_in_number_of_nos_because_n_with_superscript_o_means_that_you_know_what_never_mind_forget_it == 5:
        print("Uhhh... okay??")
    else:
        print("Done!")

words_list_upper = [line.upper() for line in words_list]
print()
print("You have a few options with which you can analyze the contents of this list below.")
print()

def prompt_user():
    print("Would you like to:\n0. Exit\n1. Search for a word\n2. Check how many times a certain combination of characters appears\n3. See what words can be created from a set of letters\n4. Generate a list of all palindromes that meet a minimum length")
    print()
    option = input("Option: ")
    return option

def take_str_input():
    query = input("Query: ")
    query = query.upper()
    return query


answer = prompt_user()
print()

while answer != '0':

    if answer == '1':
        # Determines if a word is in the list
        query = take_str_input()
        if query not in words_list_upper:
            print(f"'{query}' was not found in words.txt")
            print()
            answer = input("Select another option: ")
        else:
            index = words_list_upper.index(query)
            print(f"'{query}' is word number {index+1:,}.")
            print()
            answer = input("Select another option: ")
    
    elif answer == '2':
        # Determines how many times and in how many unique words a sequence appears.
        query = take_str_input()

        num_occurences = 0
        num_words_containing = 0
        first_occurrence_counted = False
        first_occurrence_index = 0
        containing_sequence = []

        for element in words_list_upper:
            if element.count(query) == 1:
                num_occurences += 1
                num_words_containing += 1
                if first_occurrence_counted == False:
                    first_occurrence_index = words_list_upper.index(element)
                    first_occurrence_counted = True
                containing_sequence.append(element)

            elif element.count(query) > 1:
                num_occurences += element.count(query)
                num_words_containing += 1
                if first_occurrence_counted == False:
                    first_occurrence_index = words_list_upper.index(element)
                    first_occurrence_counted = True
                containing_sequence.append(element)

        if num_occurences == 1:
            print(f"This sequence only appears one time!")
            print(f"It appears in word number {first_occurrence_index+1:,}, '{words_list_upper[first_occurrence_index]}'.")
            print()
            
        elif num_occurences > 1:
            print(f"This sequence appears {num_occurences:,} times, in {num_words_containing:,} different words.")
            print(f"It first appears in '{words_list_upper[first_occurrence_index]}' (word number {first_occurrence_index+1:,}).")
            
            print_list = input("Do you want to see the full list of words with this combination? (y/n): ")
            while print_list.upper() != 'Y' and print_list.upper() != 'N':
                print_list = input("Invalid choice. Reinput: ")
            if print_list.upper() == 'Y':
                print()
                print("Full list of words containing this sequence:")
                print(containing_sequence)
            print()
        
        else:
            print("This sequence does not appear.")
            print()

        answer = input("Select another option: ")

    elif answer =='3':
        # Determines what words can be created from a set of letters
        search_letters = input("Enter your characters in any order: ")
        letter_count = Counter(search_letters.upper())

        valid_words = []
        for word in words_list_upper:
            if not ((Counter(word)) - letter_count):
                valid_words.append(word)

        if len(valid_words) == 0:
            print("You cannot make any words with this set of letters.")
        elif len(valid_words) == 1:
            print(f"Only one word, {valid_words[0]}, can be made from this combination!")
        else:
            print(f"There are {len(valid_words)} words that can be made with the letters {list(search_letters)}. They are listed below.")
            print()
            print(valid_words)
        print()
        answer = input("Select another option: ")

    elif answer =='4':
        # Determines what words can be created from a set of characters
        num_palindromes = 0
        palindrome_length = int(input("Enter the minimum length of palindromes to search: "))
        while palindrome_length < 2:
            print("Since when does one character count as a palindrome?!")
            palindrome_length = int(input("Enter the minimum length of palindromes to search: "))
        
        palindromes = []
        for element in words_list_upper:
            if element == element[::-1] and len(element) >= palindrome_length:
                palindromes.append(element)
                num_palindromes += 1

        if num_palindromes == 1:
            print(f"There is only one palindrome, {palindromes[0]}, {palindrome_length} characters long!")
        elif num_palindromes > 1:
            print(f"There are {num_palindromes} palindromes at least {palindrome_length} characters long. They are listed below.")
            print()
            print(palindromes)
        else:
            print(f"There are no palindromes {palindrome_length} characters long.")
        

        

        print()
        answer = input("Select another option: ")
    
    else:
        print("Invalid option.")
        print()
        answer = input("Select another option: ")

end_time = time.perf_counter()
Minutes = (end_time-start_time) // 60
Seconds = (end_time-start_time) % 60
plural_min = 's'
plural_sec = 's'

if Minutes == 1:
    plural_min = ''
if round(Seconds) == 1:
    plural_sec = ''

print(f"Thank you for using this program! You spent {Minutes:,.0f} minute{plural_min} and {Seconds:,.0f} second{plural_sec} exploring the dictionary.")
print()