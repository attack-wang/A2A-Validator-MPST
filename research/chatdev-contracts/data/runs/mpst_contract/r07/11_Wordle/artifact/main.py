#!/usr/bin/env python3
"""Terminal Wordle: guess the daily 5-letter word in 6 tries."""
import datetime
import os

GREEN, YELLOW, GREY, RED = "\033[92m", "\033[93m", "\033[90m", "\033[91m"
BOLD, RESET = "\033[1m", "\033[0m"

FALLBACK = """about above abuse actor acute admit adopt adult after again agent agree ahead alarm
album alert alike alive allow alone along alter among anger angle angry ankle apart apple apply
arena argue arise armor array arrow aside asset audio audit avoid award aware badly baker bases
basic basis beach began begin begun being below bench birth black blade blame blank blast blaze
bleak blend bless blind block blood board boost booth bound brain brake brand brave bread break
breed brick bride brief bring broad broke brown brush build built bunch burst buyer cabin cable
candy canoe cargo carry carve catch cause cease chain chair chalk charm chart chase cheap check
cheek cheer chess chest chief child chill china choir chose chunk churn civic civil claim clash
class clear clerk click cliff climb cling clock close cloth cloud coach coast color comic coral
couch could count court cover crack craft crane crash crazy cream crest cross crowd crown crush
curve cycle daily dairy dance dated dealt death debut delay dense depth diary dirty dodge doing
donor doubt dozen draft drain drama drank dream dress drift drink drive drove dying eager eagle
early earth eight elbow elder elect elite empty enemy enjoy enter entry equal error event every
exact exist extra faith false fancy fault favor feast fence ferry fetch fever fewer fiber field
fiery fifth fifty fight final first fixed flame flash fleet flesh float flock flood floor flour
fluid flush focus force forge forth forty forum found frame fraud fresh fried front frost fruit
fully funny gauge ghost giant given glass gleam globe glory glove going grace grade grand grant
grape graph grasp grass grave great greed green greet grief grill grind groan group grove grown
guard guess guest guide guilt happy harsh heart heavy hedge hello hence hobby honey honor horse
hotel house human humor hurry ideal image imply index inner input issue ivory jelly jewel joint
judge juice jumbo kneel knife knock known label labor large laser later laugh layer learn lease
least leave legal lemon level lever light limit linen liver lobby local lodge logic loose lorry
lower loyal lucky lunar lunch macro magic major maker maple march match maybe mayor meant medal
media melon mercy merge merit metal meter midst might minor minus mixed model money month moral
motor mount mouse mouth movie music naive naked nasty naval nerve never newly night noble noise
north noted novel nurse occur ocean offer often olive onion opera orbit order organ other ought
ounce outer owner oxide ozone paint panel panic paper party pasta patch pause peace peach pearl
pedal penny phase phone photo piano piece pilot pinch pitch pixel pizza place plain plane plant
plate plaza plead plumb point polar porch pound power press price pride prime print prior prize
probe proof proud prove pulse punch pupil puppy purse queen query quest queue quick quiet quilt
quite quota radar radio raise rally ranch range rapid ratio reach ready realm rebel refer reign
relax relay renew reply reset resin retro rhyme rider ridge rifle right rigid rinse risky rival
river roast robin robot rocky roman rough round route royal rugby ruler rumor rural sadly saint
salad salon sauce scale scarf scene scent scope score scout scrap screw sense serve seven shade
shaft shake shall shame shape share shark sharp shave sheep sheet shelf shell shift shine shirt
shock shoot shore short shout shown sight silly since sixth sixty skill skirt skull slate sleep
slice slide slope small smart smell smile smoke snack snake sneak solar solid solve sorry sound
south space spare spark speak speed spell spend spice spike spine spite split spoke spoon sport
spray squad stack staff stage stain stair stake stale stall stamp stand stare start state steam
steel steep steer stern stick stiff still sting stock stone stood stool store storm story stove
strap straw strip study stuff style sugar suite sunny super surge swear sweat sweep sweet swept
swift swing sword table taken taste teach teeth tempo tenth thank theft their theme there these
thick thief thing think third those three threw throw thumb tiger tight times tired title toast
today token tooth topic torch total touch tough towel tower toxic trace track trade trail train
trait treat trend trial tribe trick tried tries troop trout truck truly trunk trust truth twice
twist ultra uncle under union unite unity until upper upset urban usage usual vague valid value
valve video virus visit vital vivid vocal voice voter wagon waist waste watch water weary wheat
wheel where which while white whole whose widow width witch woman women world worry worse worst
worth would wound wrist write wrong yacht yield young youth zebra"""


def load_extra():
    path = "/usr/share/dict/words"
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                return {w.strip().lower() for w in fh
                        if len(w.strip()) == 5 and w.strip().isalpha() and w.strip().islower()}
        except OSError:
            pass
    return set()


def daily_word(base):
    return base[datetime.date.today().toordinal() % len(base)]


def feedback(guess, target):
    marks = [GREY] * 5
    counts = {}
    for i, ch in enumerate(target):
        if guess[i] == ch:
            marks[i] = GREEN
        else:
            counts[ch] = counts.get(ch, 0) + 1
    for i, ch in enumerate(guess):
        if marks[i] != GREEN and counts.get(ch, 0) > 0:
            marks[i] = YELLOW
            counts[ch] -= 1
    return marks


def render(guess, marks):
    return " ".join(f"{m}{ch.upper()}{RESET}" for ch, m in zip(guess, marks))


def read_guess(wordset):
    while True:
        try:
            guess = input("Guess: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            raise SystemExit(1)
        if len(guess) != 5 or not guess.isalpha():
            print("Enter exactly 5 letters.")
        elif guess not in wordset:
            print("Not in word list.")
        else:
            return guess


def main():
    base = FALLBACK.split()
    wordset = set(base) | load_extra()
    target = daily_word(base)
    board = []
    print(BOLD + "WORDLE" + RESET + " - guess the 5-letter word in 6 tries.")
    print("Green = right letter, right spot. Yellow = right letter, wrong spot.")
    print("Grey = letter not in word. A new word is chosen each day.\n")
    for attempt in range(1, 7):
        guess = read_guess(wordset)
        board.append(render(guess, feedback(guess, target)))
        print("\n" + "\n".join(board) + "\n")
        if guess == target:
            print(GREEN + BOLD + f"You win! Solved in {attempt}/6." + RESET)
            return
    print(RED + BOLD + f"You lose. The word was {target.upper()}." + RESET)


if __name__ == "__main__":
    main()