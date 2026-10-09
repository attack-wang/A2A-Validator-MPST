import re
SAN_PATTERN = re.compile(
    r'^\s*([KQRBN])?([a-h])?([1-8])?(x)?([a-h][1-8])(?:=?([QRBN]))?[+#]?\s*$',
    re.IGNORECASE  # hmm, careful: files are lowercase a-h; if IGNORECASE then 'E4' would match piece letter... 
)