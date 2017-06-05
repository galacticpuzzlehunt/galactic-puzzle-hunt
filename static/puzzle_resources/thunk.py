# Thunk!
#
# Nathan Pinsker, 3/2017

launch_text = 'You roll your ball into the %s side of the box (i.e., %sward).\n' + \
              'You hear %s thunk%s. The ball pops out on the %s, out of hole %d.\n'

sign_text = 'The sign says:\n\n' + \
           '"Unlock the secrets of the mysterious boxes to ESCAPE THE ROOM!\n\n' + \
           'Type \'look box\' to look at the box on the table.\n' + \
           'Type \'box [number]\' to switch to a different box.\n\n' + \
           'Type \'roll [direction] [number]\' to roll your ball into the machine.\n' + \
           'The direction should be \'north\', \'south\', \'east\', or \'west\',\n' + \
           'or their single-letter abbreviations (\'n\', \'s\', \'e\', \'w\').\n\n' + \
           'Type \'box [number]\' to switch to a different box. There are 12 boxes.\n' + \
           'The first three (#1 - #3) are for practice. Try starting with those."\n'

room_text = 'You see a large instructional sign on the wall, ' + \
            'a table, a chair, and a door.\n' + \
            'You are holding a wooden ball.\n\n' + \
            'The room is spacious and bright. A box with a large \'#%s\' on it sits on a table.\n' + \
            'Eleven other boxes are sitting in a corner.\n'

help_str = 'You find yourself in a mysterious room. Your task is to ESCAPE THE ROOM!\n\n' + \
           'Type \'look\' to look around, or \'look [object]\' to look at an object.\n' + \
           'Type a COMMAND followed by a TARGET to interact with an object in the room.\n'

door_str = '''The doorway out of the room has a message on it:

___ ___, ___ ___ ___ ___ ___ ___ ___? (13)\n'''

pbox0_text = '''Discover the secrets of these boxes to escape this room!

Each box contains some number of things within --
but some of them cannot be measured!

Your task is to count how many CAN be measured.

For this box:

MEASURED: 1
MASS: 1 '''

pbox1_text = '''For this box:

MEASURED: 4
MASS: 4 '''

pbox2_text = '''For this box:

MEASURED: 4
MASS: 5 '''

# answer: 6 / 9 (BIG)
box1_text = '''Wooden boxes like this are big, heavy, and old.'''

# answer: 4 / 16 (RIG)
box2_text = '''Observe the fine rig of the curtains, the table's dancing sheen, the make of the boxes.'''

# answer: 8 / 16 (GOLD)
box3_text = '''Remember that boxes are made with care, gold leaf, and steel hinges. Only the best ingredients.'''

# answer: 10 / 12 (ATOM)
box4_text = '''Despite this box having some new rules, not an atom is misplaced.'''

# answer: 8 / 9 (SMASHED)
box5_text = '''If you seek the light, look through smashed lenses.'''

# answer: 12 / 16 (TO)
box6_text = '''Nowhere to rest your legs? Use the chair as an ottoman to find your strength again.'''

# answer: 5 / 9 (NEW)
box7_text = '''Discover the shiny brand new rules this box contains.'''

# answer: 13 / 16 (HALF)
box8_text = '''Exquisite redwood was used for lending a reserved sophistication to the top half of each box.'''

# answer: 21 / 25 (ROBOT)
box9_text = '''Xylophones also involve wood, and thunks. But xylophones are mere human creations,
while these boxes were probably made by a robot or another flawless machine.'''

practice_box0 = ['L ',
                 '  ']

practice_box1 = ['//',
                 '//']

practice_box2 = ['/ L',
                 '   ',
                 'L//']

box1 = ['/L ',
        'L//',
        '  L']

box2 = ['/L/L',
        'L  /',
        '/  L',
        'L/L/']

box3 = ['//L ',
        'L/LL',
        '/LL/',
        'LL/ ']

box4 = ['/L L',
        'L LL',
        'L///']

box5 = ['/L/',
        'L/L',
        '/L/']

box6 = [' /L ',
        '/L/L',
        'L/L/',
        ' L/ ']

box7 = ['LL/',
        '   ',
        'L /']

box8 = ['LL/L',
        ' / L',
        'L //',
        '/LL/']

box9 = ['//L//',
        'L/ L/',
        'L/L /',
        'L / L',
        '//LLL']

box_select = [ practice_box0, practice_box1, practice_box2,
               box1, box2, box3, box4, box5, box6, box7, box8, box9 ]
signs_text = [ pbox0_text, pbox1_text, pbox2_text,
               box1_text, box2_text, box3_text, box4_text, box5_text, box6_text, box7_text,
               box8_text, box9_text ]

current_index = 0
history = ''
current_box = [k for k in box_select[current_index]]

def pluralize(n):
  return 's' if n != 1 else ''

def direction_to_text(d):
  return {'e': 'east', 'w': 'west', 'n': 'north', 's': 'south', 'north': 'north', 'east': 'east', 'west': 'west', 'south': 'south'}[d]

def direction_to_abbrev(d):
  return {'e': 'e', 'w': 'w', 'n': 'n', 's': 's', 'north': 'n', 'east': 'e', 'west': 'w', 'south': 's'}[d.lower()]

def opposite(d):
  return {'e': 'w', 'w': 'e', 'n': 's', 's': 'n'}[d]

def switch_direction(d):
  return {'/': 'L', 'L': '/', ' ': ' '}[d]

def switch_if(d, if1, if2):
  if d == if1:
    return if2
  elif d == if2:
    return if1
  return d

def increment(x, y, direction):
  if direction == 'n':
    return x, y-1
  elif direction == 's':
    return x, y+1
  elif direction == 'w':
    return x-1, y
  elif direction == 'e':
    return x+1, y
  else:
    return 'Unknown increment %s' % direction

def launch(direction, row, box, should_switch = False):
  d = direction.lower()
  x, y = 0, 0
  w, h = len(box[0]), len(box)
  if d == 'n':
    x, y = row, h - 1
  elif d == 's':
    x, y = row, 0
  elif d == 'w':
    x, y = w - 1, row
  elif d == 'e':
    x, y = 0, row
  else:
    return None, 'What does "%s" mean?\n' % direction, None

  row_options = h
  if d == 'n' or d == 's':
    row_options = w
  if x < 0 or y < 0 or x >= w or y >= h:
    st = 'row' if (d == 'e' or d == 'w') else 'column'
    s = 'You can\'t roll the ball along %s %s, as the box only has %s %ss.\n' % (st, row+1, row_options, st)
    return None, s, None

  mirror_hits = 0

  while x >= 0 and y >= 0 and x < w and y < h:
    current_doodad = box[y][x]
    if current_doodad == '/':
      d = switch_if(d, 'n', 'e')
      d = switch_if(d, 'w', 's')
      mirror_hits += 1
      if should_switch:
        box[y] = box[y][:x] + 'L' + box[y][x+1:]
    elif current_doodad == 'L':
      d = switch_if(d, 'n', 'w')
      d = switch_if(d, 'e', 's')
      mirror_hits += 1
      if should_switch:
        box[y] = box[y][:x] + '/' + box[y][x+1:]
    else:
      pass
    x, y = increment(x, y, d)
  if d == 'e' or d == 'w':
    return d, y, mirror_hits
  return d, x, mirror_hits


def gen_examine_box_str(index, box):
  w = len(box[0])
  h = len(box)
  return ('A mysterious box with a %s pattern on it.\n' + \
         'The box has a large \'#%s\' on the side, and a small placard ' + \
         'underneath with something etched on it.\n' + \
         'The box is %s by %s.\n' + \
         'It has %s holes on each of its west and ' + \
         'east sides (labeled 1 through %s running north to south).\n' + \
         'It has %s holes on each of its north and ' + \
         'south sides (labeled 1 through %s running west to east).\n') % ('calm' if index <= 6 else 'swirling' if index <= 9 else 'torrential',
                                                                           index, w, h, h, h, w, w)

def handle_input(input_text, current, hist):
  global current_index
  global current_box
  global history
  current_index = current
  history = hist

  s = input_core(input_text)
  return {'content': s,
          'currentBox': current_index,
          'history': history}


def input_core(input_text):
  global current_index
  global current_box
  global history

  input_text = input_text.split(' ')
  current_box = [k for k in box_select[current_index]]
  if input_text[0] == 'help':
    return help_str
  elif 'semiautomaton' in input_text:
      return 'You say the word aloud, and the door hisses open. ' + \
             'Looks like you have your answer to this puzzle!\n'
  elif input_text[0] == 'look' or input_text[0] == 'examine' or input_text[0] == 'l' or input_text[0] == 'e':
    if len(input_text) > 1 and (len(input_text) > 2 or input_text[1] != 'around'):
      target = ' '.join(input_text[1:])
      if target == 'box' or target == 'machine' or target == 'thing':
        return gen_examine_box_str(current_index+1, current_box)
      elif target == 'boxes':
        return 'Boxes with labels from 1-12, except for #%s, which is on the table.\n' % (current_index+1)
      elif target == 'table':
        return 'The table is made of oak. It stands steadfast and strong.\n'
      elif target == 'door':
        return door_str
      elif 'sign' in target:
        return sign_text
      elif target == 'placard':
        return signs_text[current_index] + '\n'
      elif 'ball' in input_text:
        return 'The ball is smooth, polished, and heavy in your hand.\n' + \
              'Roll it into a box by typing "roll [direction] [number]".\n'
      elif target == 'chair':
        return 'Made of wood, but seems a little flimsy.\n'
      elif target == 'table':
        return 'A very high-quality oaken table, about two inches thick and ' + \
              'with four sturdy legs.\n'
      elif target == 'room':
        return room_text % (current_index+1)
      else:
        return 'I don\'t know what you\'re trying to look at.\n'
    else:
      return room_text % (current_index+1)
  elif input_text[0] == 'talk':
    return 'Nobody in this room to talk to but yourself, sport.\n'
  elif input_text[0] == 'box' or input_text[0] == 'switch' or input_text[0] == 'ask':
    if len(input_text) == 0 or not input_text[-1].isdigit():
      return 'You throw some punches at the air.\n'
    else:
      index = int(input_text[-1]) - 1
      if index >= 0 and index < len(box_select):
        if index != current_index:
          old_index = current_index
          current_index = index
          history = ''
          current_box = [k for k in box_select[index]]
          return 'You put box #%s in the corner. You take box #%s and put it on the table.\n' % (old_index+1, index+1)
        else:
          return 'Box #%s is already on the table.\n' % (index+1)
      else:
        return 'You attempt to find box #%s, but to no avail.\n' % (index+1)
  elif input_text[0] == 'fire' or input_text[0] == 'ball' or input_text[0] == 'roll' or input_text[0] == 'launch':
    hist_split = [[history[i], int(history[i+1])] for i in range(0, len(history), 2)]
    for d, r in hist_split:
      launch(d, r, current_box, (current_index >= 9))
      if current_index >= 6 and current_index < 9:
          for i in range(len(current_box)):
            current_box[i] = [switch_direction(k) for k in current_box[i]]

    if len(input_text) >= 3 and input_text[2].isdigit():
      input_text[1] = direction_to_abbrev(input_text[1])
      d, row, hits = launch(input_text[1], int(input_text[2]) - 1, current_box, (current_index >= 9))
      if d:
        s = launch_text % (direction_to_text(opposite(input_text[1])),
                             direction_to_text(input_text[1]),
                             hits, pluralize(hits),
                             direction_to_text(d), row+1)
        if current_index >= 6 and current_index < 9:
          for i in range(len(current_box)):
            current_box[i] = [switch_direction(k) for k in current_box[i]]
        history += input_text[1] + str(int(input_text[2])-1)
        return s
      else:
        return row
    elif len(input_text) >= 3 and input_text[1].isdigit():
      # lol
      input_text[2] = direction_to_abbrev(input_text[2])
      d, row, hits = launch(input_text[2], int(input_text[1]) - 1, current_box, (current_index >= 9))
      if d:
        s = launch_text % (direction_to_text(opposite(input_text[2])),
                             direction_to_text(input_text[2]), hits, pluralize(hits),
                             direction_to_text(d), row+1)
        if current_index >= 6 and current_index < 9:
          for i in range(len(current_box)):
            current_box[i] = [switch_direction(k) for k in current_box[i]]
        history += input_text[2] + str(int(input_text[1])-1)
        return s
      else:
        return row
    else:
      return 'You can\'t roll like that. Try \'roll [direction] [number]\'.\n'
  elif input_text[0] == 'open':
    if input_text[1] == 'door':
      return 'The door is locked, unsurprisingly, but you see something on it.\n'
    else:
      return 'That doesn\'t look like it can be opened.'
  elif input_text[0] == 'take':
    return 'You already have everything you need right now.\n'
  else:
    return 'Sorry, that command doesn\'t work. Type \'help\' for help.\n'

if __name__ == '__main__':
  while True:
    print input_core(raw_input('>> '))
