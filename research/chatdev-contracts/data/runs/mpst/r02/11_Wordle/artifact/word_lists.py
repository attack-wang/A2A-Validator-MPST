'''
word_lists.py
Curated word lists for the Wordle game.
ANSWER_WORDS: common 5-letter English words that can be chosen as the
    daily secret answer.
EXTRA_VALID_WORDS: additional 5-letter English words that are accepted
    as guesses but are never selected as the answer.
VALID_GUESS_WORDS: the union of both lists, used for guess validation.
'''
ANSWER_WORDS = """
about above abuse actor acute admit adopt adult after again agent agree
ahead alarm album alert alike alive allow alone along alter among anger
angle angry apart apple apply arena argue arise armor aroma array arrow
aside asset atlas audio audit avoid awake award aware badly baker basic
basis beach beard beast began begin being belly below bench berry birth
black blade blame blank blast blind block bloom blues blunt blush board
boast bonus boost booth bound brain brake brand brave bread break breed
brick bride brief bring brisk broad broke brook brown brush build built
bunch burst buyer cabin cable camel candy canoe cargo carry carve catch
cause cease cedar chain chair chalk charm chart chase cheap check cheek
cheer chess chest chief child chill choir chose chunk cider cigar civic
civil claim clash clasp class clean clear clerk click cliff climb cloak
clock close cloth cloud coach coast cobra cocoa colon color comet comic
coral couch cough could count court cover crack craft crane crash crawl
crazy cream creek crest crime crisp cross crowd crown crumb crush curve
cycle daily dairy dance dated dealt death debut delay depth derby devil
diary dirty dodge donor doubt dozen draft drain drama drank drape drawn
dream dress dried drift drill drink drive drove drown drunk dusty dwarf
eager eagle early earth eight elbow elder elect elite empty enemy enjoy
enter entry equal equip erase error erupt essay event every exact exile
exist extra fable faith fancy fatal fault favor feast fence ferry fever
fiber field fifth fifty fight final first flame flash fleet flesh flick
fling flood floor flour fluid flute focus foggy force forge forth forty
forum found frame fraud fresh front frost fruit fully funny gauge ghost
giant given glass globe glory glove going goose grace grade grain grand
grant grape graph grasp grass grave great green greet grief grill grind
group grove growl grown guard guess guest guide guilt happy harsh heart
heavy hedge hello hence hobby honey honor horse hotel house human humor
hurry ideal image imply index inner input issue ivory jelly jewel joint
judge juice juicy kneel knife knock known label labor large laser later
laugh layer learn lease least leave legal lemon level light limit linen
liver local lodge logic loyal lucky lunar lunch lying magic major maker
maple march match mayor meant medal media mercy merge merit merry metal
meter might minor minus mixed model moist money month moral motor mount
mouse mouth movie music naive naked nasty naval nerve never newly night
noble noise north notch novel nurse oasis occur ocean offer often olive
onion onset opera orbit order organ other otter ought ounce outer owner
oxide ozone paint panel panic paper party pasta paste patch pause peace
peach pearl pedal penny phase phone photo piano piece pilot pinch pitch
pivot pixel place plain plane plant plate plaza plead plumb plume point
polar porch pouch pound power press price pride prime print prior prism
prize probe prone proof proud prove pulse punch pupil puppy purse queen
query quest queue quick quiet quilt quite quota quote radar radio raise
rally ranch range rapid ratio reach react ready realm rebel refer reign
relax relay reply resin rhyme rider ridge rifle right rigid risky rival
river roast robin robot rocky rough round route royal rugby ruler rumor
rural sadly salad salon sauce scale scarf scene scent scope score scout
scrap screw sense serve seven shade shaft shake shall shame shape share
shark sharp shave shelf shell shift shine shiny shirt shock shore short
shout shown sight silly since sixth sixty skill skirt slate sleep slice
slide slope small smart smell smile smoke snack snake sneak solar solid
solve sonic sound south space spare spark speak speed spell spend spice
spike spine split spoke spoon sport spray squad stack staff stage stain
stair stake stand start state steam steel steep steer stern stick stiff
still stock stone stood store storm story stove strap straw strip study
stuff style sugar suite sunny super surge swear sweat sweep sweet swell
swift swing sword table taken taste teach teeth tempo tenth thank theft
theme there these thick thief thing think third those three threw throw
thumb tiger tight timer title toast today token torch total touch tough
towel tower trace track trade trail train trait treat trend trial tribe
trick troop truck truly trunk trust truth tulip tumor tutor twice twist
ultra uncle union unite unity upper upset urban usage usual valid value
video virus visit vital vivid vocal voice voter wagon waste watch water
weary weave wedge weigh weird whale wheat wheel where which while white
whole whose widow width witch woman world worry worse worst worth would
wound wrist write wrong wrote yacht yield young youth zebra
""".split()
EXTRA_VALID_WORDS = """
aback abase abate abbey abbot abhor abide abled abode abort abyss acorn
acrid acted adage adapt added adder adept adieu adobe adore adorn aegis
aerie affix afire afoot agile aglow agony aider aisle alder alien align
alley allot alloy aloft aloof altar amass amaze amble amend amiss amity
ample amuse angel ankle annex annoy annul anode antic anvil aorta apnea
apron aptly arbor ardor argon arose arson artsy ascot ashen ashes aspic
assay atoll atone attic augur aunty avail avert avian await awash awful
awoke axiom azure bagel baggy balmy banal barge baron basil basin baste
bathe baton bayou beady beech befit beget beige belie belle beret beset
betel bevel bezel bible bicep bigot bilge bingo biome birch bison bitty
blare bleak bleat bleed bleep blimp blink bliss bloat blurb blurt bobby
bogey bogus bolus bongo bonny bosom botch bough boule bowel boxer brace
braid brawn briar brier brine briny bravo brawl briar...