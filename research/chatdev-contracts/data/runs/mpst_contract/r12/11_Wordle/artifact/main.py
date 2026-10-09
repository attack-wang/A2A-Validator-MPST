#!/usr/bin/env python3
"""Terminal Wordle: guess the daily 5-letter word in 6 tries."""
import datetime
import random

WORDS = set("""about above abuse actor acute admit adopt adult after again agent agree ahead alarm
album alert alike alive allow alone along alter among anger angle angry apart apple apply arena
argue arise armor aroma array arrow aside asset audio audit avoid award aware badly baker basic
basis beach began begin being below bench birth black blade blame blank blast blind block blood
board boost booth bound brain brand bread break breed brief bring broad broke brown brush build
built bunch burst buyer cabin cable candy canoe cargo carry catch cause chain chair chalk charm
chart chase cheap check cheek cheer chess chest chief child chill choir chose civil claim clash
class clean clear clerk click cliff climb cling clock close cloth cloud coach coast color comet
comic coral couch could count court cover crack craft crash crawl crazy cream creek crime crisp
cross crowd crown crush curve cycle daily dairy dance dealt death debut decay delay depth diary
dirty dodge doubt dozen draft drain drama drank dream dress drift drink drive drove eager eagle
early earth eight elbow elder elect elite empty enemy enjoy enter entry equal error event every
exact exist extra faith false fault favor feast fence ferry fetch fever fewer fiber field fifth
fifty fight final first flame flash fleet flesh float flood floor flour fluid flute focus force
forge forth forty forum found frame fraud fresh front frost fruit fully funny giant given glass
globe glory glove going goose grace grade grain grand grant grape graph grasp grass grave great
green greet grill grind group guard guess guest guide habit happy harsh heart heavy hello hence
hobby honey honor horse hotel house human humor hurry ideal image imply index inner input issue
ivory jelly jewel joint judge juice kneel knife knock known label labor large laser later laugh
layer learn lease least leave legal lemon level light limit linen liver local lodge logic loose
lower loyal lucky lunar lunch lyric magic major maker maple march match mayor meant medal media
mercy merge merit merry metal meter might minor minus mixed model money month moral motor mount
mouse mouth movie music naive naval nerve never newly night noble noise north novel nurse occur
ocean offer often olive onion onset opera orbit order organ other ounce outer owner paint panel
paper party pasta patch pause peace peach pearl pedal penny phase phone photo piano piece pilot
pinch pitch pizza place plain plane plant plate plaza point polar porch pound power press price
pride prime print prize proof proud prove pulse punch pupil queen quest queue quick quiet quilt
quote radar radio raise rally ranch range rapid ratio reach ready realm rebel refer reign relax
reply rhyme rider ridge rifle right rigid risky rival river roast robin robot rocky roman rough
round route royal rural salad salon sauce scale scene scent scope score scout scrap screw sense
serve seven shade shaft shake shall shame shape share shark sharp sheep sheet shelf shell shift
shine shirt shock shoot shore short shown sight silly since sixth sixty skill skirt sleep slice
slide slope small smart smell smile smoke snack snake solar solid solve sorry sound south space
spare spark speak speed spell spend spice spike split spoke sport spray squad staff stage stain
stair stake stand start state steam steel steep steer stick still stock stone stood store storm
story stove strap straw strip study stuff style sugar suite sunny super sweet sweep swift swing
sword table taken taste teach teeth tempo tenth thank theft their theme there these thick thief
thing think third those three threw throw thumb tiger tight timer title toast today token tooth
topic total touch tough towel tower toxic trace track trade trail train treat trend trial tribe
trick tried truck truly trunk trust truth tulip tutor twist ultra uncle under union unite unity
until upper upset urban usage usual valid value video virus visit vital vivid vocal voice vowel
wagon waste watch water wheel where which while white whole whose widow width witch woman world
worry worse worst worth would wound wrist write wrong wrote yacht yield young youth zebra""".split())

MAX_ATTEMPTS = 6
WORD_LEN = 5
GREEN = "\033[1;37;42m"
YELLOW = "\033[1;37;43m"
GREY = "\033[1;37;100m"
RESET = "\033[0m"
RANK = {GREY: 0, YELLOW: 1, GREEN: 2}


def daily_word():
    rng = random.Random(datetime.date.today().isoformat())
    return sorted(WORDS)[rng.randrange(len(WORDS))]


def feedback(guess, answer):
    marks = [GREY] * WORD_LEN
    counts = {}
    for i in range(WORD_LEN):
        if guess[i] == answer[i]:
            marks[i] = GREEN
        else:
            counts[answer[i]] = counts.get(answer[i], 0) + 1
    for i in range(WORD_LEN):
        if marks[i] != GREEN and counts.get(guess[i], 0) > 0:
            marks[i] = YELLOW
            counts[guess[i]] -= 1
    return marks


def render(guess, marks):
    return " ".join("%s %s %s" % (m, g, RESET) for g, m in zip(guess, marks))


def update_keyboard(kb, guess, marks):
    for g, m in zip(guess, marks):
        if RANK[m] > RANK[kb.get(g, GREY)]:
            kb[g] = m


def show_keyboard(kb):
    print(" " + " ".join("%s %s %s" % (kb.get(c, GREY), c.upper(), RESET) for c in "qwertyuiop"))
    print("   " + " ".join("%s %s %s" % (kb.get(c, GREY), c.upper(), RESET) for c in "asdfghjkl"))
    print("     " + " ".join("%s %s %s" % (kb.get(c, GREY), c.upper(), RESET) for c in "zxcvbnm"))


def show_board(guesses):
    print()
    for g, m in guesses:
        print("  " + render(g, m))
    for _ in range(MAX_ATTEMPTS - len(guesses)):
        print("  " + " ".join("·" for _ in range(WORD_LEN)))


def main():
    answer = daily_word()
    print("=" * 40)
    print(" WORDLE - " + datetime.date.today().strftime("%Y-%m-%d"))
    print(" Guess the 5-letter word in 6 tries.")
    print(" " + GREEN + " G " + RESET + " right spot   " + YELLOW + " Y " + RESET +
          " wrong spot   " + GREY + " X " + RESET + " not in word")
    print(" Enter a 5-letter word, or 'q' to quit.")
    print("=" * 40)
    guesses, kb = [], {}
    while len(guesses) < MAX_ATTEMPTS:
        show_board(guesses)
        show_keyboard(kb)
        try:
            guess = input("\nGuess %d/%d: " % (len(guesses) + 1, MAX_ATTEMPTS)).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye! The word was %s." % answer)
            return
        if guess == "q":
            print("The word was %s." % answer)
            return
        if len(guess) != WORD_LEN or not guess.isalpha():
            print("Invalid guess: enter exactly 5 letters.")
            continue
        if guess not in WORDS:
            print("Invalid guess: not in the word list.")
            continue
        marks = feedback(guess, answer)
        guesses.append((guess, marks))
        update_keyboard(kb, guess, marks)
        if guess == answer:
            show_board(guesses)
            print("\nYou won in %d/%d! The word was %s." % (len(guesses), MAX_ATTEMPTS, answer))
            return
    show_board(guesses)
    show_keyboard(kb)
    print("\nOut of attempts. The word was %s." % answer)


if __name__ == "__main__":
    main()