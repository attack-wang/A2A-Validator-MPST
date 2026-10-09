import re
CASTLE_KING = re.compile(r'^(O-O|0-0)$')
CASTLE_QUEEN = re.compile(r'^(O-O-O|0-0-0)$')
PIECE_MOVE = re.compile(r'^([KQRBN])([a-h]?)([1-8]?)(x?)([a-h][1-8])$')
PAWN_MOVE = re.compile(r'^(?:([a-h])?(x))?([a-h][1-8])(?:=([QRBN]))?$')