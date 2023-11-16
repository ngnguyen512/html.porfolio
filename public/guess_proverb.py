import random
import collections
 
def load_proverbs(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if lines:
                proverbs = [line.strip() for line in lines]
            else:
                print('Proverbs file is empty.')    
                return None
        return proverbs
    
    except:
        print("Proverbs file not found.")
        return None  
 
def get_proverb(proverbs):
    proverb = random.choice(proverbs)
    return proverb
    
 
def get_current_masked(proverb, masked):
    ret = ""
    for c, is_masked in zip(proverb, masked):
        ret += '~' if is_masked else c
    return ret
 
def get_raw_lower_words(proverbs, masked):
    ret = ""
    for c, is_masked in zip(proverbs, masked):
        if is_masked or c == "'":
            ret += c.lower()
        else:
            ret += '|'
    return [word for word in ret.split("|") if len(word.strip()) > 0]
 
def reveal_words(guess, masked, indicies):
    for index in indicies[guess]:
        for i in range(index, index + len(guess)):
            masked[i] = False
 
# Reveal least frequent, unrevealed character
def reveal_char(proverb, masked):
    unreveal_chars = [c.lower() for i, c in enumerate(proverb) if masked[i]]
    char_counter = dict(collections.Counter(unreveal_chars))
 
    # Find the min frequency char
    min_frequency = len(proverb) + 1
    char_to_reveal = None
    for c, frequency in char_counter.items():
        if frequency < min_frequency:
            min_frequency = frequency
            char_to_reveal = c
 
    # Actually reveal them
    for i, c in enumerate(proverb):
        if masked[i] and c.lower() == char_to_reveal:
            masked[i] = False
 
 
# Return number of wrongs and reveals
def guess_input(proverb, masked, indicies, guesses_left, user_input, misses):
    wrong_guesses = 0
    user_guess = user_input.lower().split()
    reveals = 0
    print_misses = False
 
    for guess in user_guess:
        if guess in indicies:
            print("Good guess!", '"' + guess + '"', "is in the proverb.")
            reveal_words(guess, masked, indicies)
        else:
            misses.append(guess)
            print_misses = True
            wrong_guesses += 1
            guesses_left -= 1
            reveal_char(proverb, masked)
            if guesses_left < 0:
                break
    if print_misses:
        print(f"Misses: {', '.join(misses)}")
    if len(user_input) == 0:
        print("No guess:")
        wrong_guesses += 1
        guesses_left -= 1
        reveal_char(proverb, masked)
    return wrong_guesses
 
def build_word_indicies(proverb):
    lower_proverb = proverb.lower()
    indicies = collections.defaultdict(list)
 
    current_word = ""
    start_index = None
    for i, c in enumerate(lower_proverb + " "):
        if c.isalpha() or c == "'":
            if start_index is None:
                start_index = i
            current_word += c.lower()
        else:
            indicies[current_word].append(start_index)
            start_index = None
            current_word = ""
 
    return dict(indicies)
 
def printStats(rounds_played, rounds_won, total_reveal, total_words):
    win_percentage = (rounds_won / rounds_played) * 100
    average_letter_reveal = (total_reveal / total_words) * 100
    print(f"Your stats so far:")
    print(f"Rounds played: {rounds_played}")
    print(f"Rounds won: {win_percentage}%")
    print(f"Total reveals: {total_reveal}")
    print(f"Average letter reveal: {average_letter_reveal}%")
 
def main():
    proverbs = load_proverbs('proverbs.txt')
    misses = []
    rounds_played = 0
    rounds_won = 0
    total_reveal = 0
    total_words = 0
    while True:
        rounds_played += 1
        proverb = get_proverb(proverbs)
 
        masked = [c.isalpha() for c in proverb]
        raw_words = get_raw_lower_words(proverb, masked)
        indicies = build_word_indicies(proverb)
 
        wrong_guess = 0
        max_guess = len(raw_words)
        total_words += len(raw_words)
 
        while wrong_guess < max_guess and any(masked):
            print(get_current_masked(proverb, masked))
            print("letter reveals : %d / %d" % (wrong_guess, max_guess))
            user_input = input(">> Guess: ")
            wrong_guess += guess_input(proverb, masked, indicies, max_guess - wrong_guess + 1, user_input, misses)
 
        if wrong_guess >= max_guess:
            print("Sorry, you have lost this round.")
        else:
            print("Congratulations, you won this round!")
            rounds_won += 1
 
        total_reveal += wrong_guess
        masked = [False] * len(proverb)
        print("The proverb is:", get_current_masked(proverb, masked))
        printStats(rounds_played, rounds_won, total_reveal, total_words)
        play_again = input("Play again? (Y/N) ")
        if play_again.lower() != 'y' and play_again.lower() != 'n':
            print("Invalid Input.Try again")
            play_again = input("Play again? (Y/N) ")
            if play_again.lower() == 'n':
                print("Another time")
                break  
        elif play_again.lower() != 'y' and play_again.lower() == 'n':
            print("Another time")
            break
if __name__ == "__main__":
    main()