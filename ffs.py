import re
import sys
import json
from itertools import chain, product

LEFT = (('S',     's'),
        ('S*',    'z'), # put S* after S so that S*ET, e.g., is "zet", not "seth"
        ('ST',    'st'),
        ('STP',   'sf'),
        ('STPH',  'sn'),
        ('SK',    'sk'),
        ('SKP',   'exp'),  # special
        ('SKW',   'squ'),  # special
        ('SKWR',  'j'),
        ('SKH',   'sch'),
        ('SKR',   'sc'),   # skr? scr?
        ('SP',    'sp'),
        ('SPW',   'int'),  # ent?
        ('SPWR',  'intr'), # entr?
        ('SPH',   'sm'),
        ('SPHR',  'spl'),
        ('SPR',   'spr'),
        ('SW',    'sw'),
        ('SH',    'sh'),
        ('SHR',   'sl'),   # shr?
        ('SR',    'v'),
        ('T',     't'),
        ('TK',    'd'),
        ('TKPW',  'g'),
        ('TKPWH', 'gh'),
        ('TKPWR', 'gr'),
        ('TP',    'f'),
        ('TPH',   'n'),
        ('TPHR',  'fl'),
        ('TPR',   'fr'),
        ('TW',    'tw'),
        ('TH',    'th'),
        ('THR',   'tl'),   # thr? but tle is useful
        ('TR',    'tr'),
        ('K',     'k'),
        ('KP',    'x'),
        ('KPW',   'imp'),  # imb? emp? emb?
        ('KPWHR', 'impl'),
        ('KPWR',  'impr'),
        ('KW',    'q'),    # kw? qu?
        ('KWR',   'y'),
        ('KH',    'ch'),
        ('KHR',   'kl'),   # chr?
        ('KR',    'c'),
        ('P',     'p'),
        ('PW',    'b'),
        ('PWH',   'bh'),
        ('PWHR',  'bl'),
        ('PWR',   'br'),
        ('PH',    'm'),
        ('W',     'w'),
        ('WH',    'wh'),
        ('WR',    'wr'),
        ('H',     'h'),
        ('HR',    'l'),
        ('R',     'r'))

MID = (('A',    'a'),
       ('AO',   'oo'), # oa?
       ('AOE',  'ee'),
       ('AOEU', 'y'),  # ai?
       ('AE',   'ea'), # ae?
       ('AEU',  'ai'), # ay?
       ('AU',   'au'),
       ('O',    'o'),
       ('OE',   'oe'),
       ('OEU',  'oi'), # oy?
       ('OU',   'ou'),
       ('E',    'e'),
       ('EU',   'i'),
       ('U',    'u'))

RIGHT = (('F',     'f'),
         ('FR',    'fr'),
         ('FRP',   'mp'),
         ('FRPB',  'nch'),  # rch?
         ('FRPT',  'mpt'),
         ('FRPTS', 'mpts'),
         ('FRPS',  'mps'),
         ('FRB',   'rv'),   # rve?
         ('FP',    'ch'),
         ('FL',    'fl'),
         ('FT',    'ft'),   # st?
         ('FS',    'fs'),
         ('R',     'r'),
         ('RP',    'rp'),
         ('RPB',   'rn'),
         ('RPBLG', 'rj'),   # rge?
         ('RPBS',  'rns'),
         ('RPS',   'rps'),
         ('RB',    'sh'),   # rb?
         ('RBS',   'rbs'),
         ('RL',    'rl'),
         ('RLT',   'rlt'),
         ('RLTS',  'rlts'),
         ('RLS',   'rls'),
         ('RLD',   'rld'),
         ('RLDZ',  'rlds'),
         ('RG',    'rg'),
         ('RGS',   'rgs'),
         ('RT',    'rt'),
         ('RTS',   'rts'),
         ('RS',    'rs'),
         ('RD',    'rd'),
         ('RDZ',   'rds'),
         ('RZ',    'rz'),
         ('P',     'p'),
         ('PB',    'n'),
         ('PBL',   'nl'),
         ('PBLG',  'j'),
         ('PBG',   'ng'),
         ('PBGS',  'ngs'),
         ('PBT',   'nt'),
         ('PBTS',  'nts'),
         ('PBS',   'ns'),
         ('PBD',   'nd'),
         ('PBDZ',  'nds'),
         ('PBZ',   'nz'),
         ('PL',    'm'),
         ('PLT',   'mt'),
         ('PT',    'pt'),
         ('PTS',   'pts'),
         ('PS',    'ps'),
         ('B',     'b'),
         ('BL',    'bl'),
         ('BG',    'k'),
         ('BGS',   'ks'),   # ction?
         ('BT',    'bt'),
         ('BTS',   'bts'),
         ('BS',    'bs'),
         ('L',     'l'),
         ('LG',    'lg'),
         ('LT',    'lt'),
         ('LS',    'ls'),
         ('LD',    'ld'),
         ('LDZ',   'lds'),
         ('LZ',    'lz'),
         ('G',     'g'),
         ('GS',    'gs'),   # tion?
         ('T',     't'),
         ('TS',    'ts'),
         ('S',     's'),
         ('D',     'd'),
         ('DZ',    'ds'),
         ('Z',     'z'),
         ('*PBG',  'nk'),
         ('*PBGS', 'nks'),
         ('*PL',   'mp'),
         ('*PLT',  'mpt'),
         ('*PLTS', 'mpts'),
         ('*PLS',  'mps'),
         ('*LG',   'lk'),
         ('*LGS',  'lks'),
         ('*T',    'th'),
         ('*TS',   'ths'))

dictionary = {}

for left, mid, right in product(*(chain(strokes, (None,))
                                  for strokes in (LEFT, MID, RIGHT))):
    bridge = ''

    if mid is None and right is not None:
        bridge = '-'

    leftkey,  leftval  = left  if left  is not None else ('', '')
    midkey,   midval   = mid   if mid   is not None else ('', '')
    rightkey, rightval = right if right is not None else ('', '')

    midleftkey, midrightkey = re.match(r'(A?O?)(E?U?)', midkey).groups()

    if '*' in leftkey and '*' in rightkey:
        continue
    if '*' in leftkey:
        leftkey = leftkey.replace('*', '')
        bridge = '*'
    elif '*' in rightkey:
        rightkey = rightkey.replace('*', '')
        bridge = '*'

    key = leftkey + midleftkey + bridge + midrightkey + rightkey
    if not key:
        continue
    value = leftval + midval + rightval
    dictionary[key] = f'{{&{value}}}'

assert '' not in dictionary

tests = (('S',      '{&s}'),
         ('T',      '{&t}'),
         ('-T',     '{&t}'),
         ('-S',     '{&s}'),
         ('AT',     '{&at}'),
         ('S-T',    '{&st}'),
         ('S*ET',   '{&zet}'),
         ('PHA*T',  '{&math}'),
         ('SKHAOL', '{&school}'),
         ('HRAEUT', '{&lait}'),
         ('ROEPBT', '{&roent}'))

for key, val in tests:
    assert dictionary.get(key) == val

json.dump(dictionary, sys.stdout, indent=0)
