#!/usr/bin/env python3
"""Terminal Wordle: guess the daily 5-letter word in 6 tries."""
import datetime
import random
import sys

WORDS = """about above actor acute admit adopt adult after again agent agree ahead alarm
album alert alike alive allow alone along alter among anger angle angry ankle apart apple
apply arena argue arise armor array arrow aside asset audio audit avoid awake award aware
badly baker basic beach beard beast begin being below bench berry birth black blade blame
blank blast bleed blend blind block blood board boost booth bound brain brand bread break
breed brick brief bring broad broke brown brush build built bunch burst buyer cabin cable
candy carry catch cause chain chair chalk charm chart chase cheap check cheek cheer chess
chest chief child chill chose claim class clean clear clerk click cliff climb clock close
cloth cloud coach coast color comic coral couch could count court cover crack craft crash
cream crime crisp cross crowd crown curve cycle daily dance dealt death debut delay dense
depth diary dirty dodge doing donor doubt dozen draft drain drama drank dream dress drift
drill drink drive drove drown dryer eager early earth eight elbow elder elect enemy enjoy
enter entry equal error event every exact exist extra faith false fancy fault favor feast
fence ferry fever field fiery fifth fifty fight final first flame flash fleet flesh float
flood floor flour fluid focus force forth forty forum found frame fraud fresh front fruit
fully funny gauge ghost giant given glass globe glory glove going goose grace grade grain
grand grant grape graph grasp grass grave great green greet grief grill grind group guard
guess guest guide happy harsh heart heavy hedge hello hence hobby honey honor horse hotel
house human humor hurry ideal image imply index inner input issue ivory jelly jewel joint
judge juice kneel knife knock known label labor large laser later laugh layer learn lease
least leave legal lemon level light limit linen liver local lodge logic loose lorry lower
loyal lucky lunar lunch macro magic major maker maple march match maybe mayor meant medic
mercy merge merit metal meter might minor minus mixed model money month moral motor mount
mouse mouth movie music naive nasty naval nerve never newly night noble noise north noted
novel nurse occur ocean offer often olive onion onset opera orbit order organ other ought
ounce outer owner paint panel paper party pasta patch pause peace peach pearl pedal penny
phase phone photo piano piece pilot pinch pitch pixel place plain plane plant plate plaza
point polar porch pound power press price pride prime print prize probe prone proof proud
prove pulse punch pupil purse queen query quest queue quick quiet quite quota radar radio
raise rally ranch range rapid ratio reach ready realm rebel refer reign relax reply resin
rhyme rider ridge rifle right rigid rinse risky rival river roast robin robot rocky rough
round route royal rugby ruler rumor rural sadly salad salon sauce scale scene scent scope
score scout scrap screw seize sense serve seven shade shaft shake shall shame shape share
sharp sheep sheet shelf shell shift shine shiny shirt shock shoot shore short shout shown
shrug sight silly since siren sixth sixty skill skirt slate sleep slice slide slope small
smart smell smile smoke snack snake sneak solar solid solve sorry sound south space spare
spark speak speed spell spend spice spike spine spite split spoke spoon sport spray squad
stack staff stage stain stair stake stale stall stamp stand stare start state steam steel
steep steer stern stick stiff still sting stock stone stood stool store storm story stout
stove strap straw strip study stuff style sugar suite sunny super surge swamp swarm swear
sweat sweep sweet swept swift swing sword table taken taste teach teeth tempo tenor tense
thank theft their theme there these thick thief thigh thing think third those three threw
throw thumb tiger tight timer times tired title toast today token torch total touch tough
tower toxic trace track trade trail train trait trash treat trend trial tribe trick tried
troop trout truck truly trunk trust truth tulip tutor twice twist ultra uncle under union
unite unity until upper upset urban usage usual vague valid value valve vapor vault venue
verse video vigor villa vinyl viral virus visit vital vivid vocal voice voter wagon waist
waste watch water weary wedge weird whale wheat wheel where which while white whole whose
widow width witch woman world worry worse worst worth would wound wrist write wrong yacht
yield young youth zebra""".split()

GREEN, YELLOW, GREY, RESET, BOLD = "\033[92m", "\033[93m", "\033[90m", "\033[0m", "\033[1m"
MAX_TRIES = 6


def feedback(guess, answer):
    """Return per-letter colors: green/yellow/grey with duplicate handling."""
    colors = [GREY] * 5
    remaining = {}
    for i, ch in enumerate(answer):
        if guess[i] != ch:
            remaining[ch] = remaining.get(ch, 0) + 1
    for i, ch in enumerate(guess):
        if ch == answer[i]:
            colors[i] = GREEN
        elif remaining.get(ch, 0) > 0:
            colors[i] = YELLOW
            remaining[ch] -= 1
    return colors


def render(guess, colors):
    return " ".join(f"{c}{ch.upper()}{RESET}" for ch, c in zip(guess, colors))


def daily_word():
    rng = random.Random(datetime.date.today().toordinal())
    return rng.choice(WORDS)


def main():
    answer = daily_word()
    print(f"{BOLD}=== WORDLE ==={RESET}")
    print("Guess the 5-letter word. You have 6 tries.")
    print("Green = right letter, right spot | Yellow = right letter, wrong spot | Grey = not in word")
    print(f"Today is {datetime.date.today().isoformat()}; everyone gets the same daily word.\n")

    for turn in range(1, MAX_TRIES + 1):
        while True:
            try:
                guess = input(f"Guess {turn}/{MAX_TRIES}: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print(f"\nGoodbye! The word was: {answer.upper()}")
                return
            if len(guess) == 5 and guess.isalpha() and guess in WORDS:
                break
            print("Invalid guess: enter a 5-letter English word from the dictionary.")

        print(" " * len(f"Guess {turn}/{MAX_TRIES}: ") + render(guess, feedback(guess, answer)))
        if guess == answer:
            print(f"\n{GREEN}{BOLD}You win!{RESET} You guessed it in {turn} try"
                  f"{'ies' if turn > 1 else ''}.")
            return

    print(f"\n{BOLD}Out of tries.{RESET} The word was: {GREEN}{BOLD}{answer.upper()}{RESET}")


if __name__ == "__main__":
    main()