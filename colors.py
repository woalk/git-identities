class Colors:
    _esc = '\033['

    _style_no = 0
    _style_bold = 1
    _style_underline = 2
    _style_negative1 = 3
    _style_negative2 = 5

    _fcolor_black = 30
    _fcolor_red = 31
    _fcolor_green = 32
    _fcolor_yellow = 33
    _fcolor_blue = 34
    _fcolor_purple = 35
    _fcolor_cyan = 36
    _fcolor_white = 37
    _fcolor_gray = 90
    _fcolor_bred = 91
    _fcolor_bgreen = 92
    _fcolor_byellow = 93
    _fcolor_bblue = 94
    _fcolor_bpurple = 95
    _fcolor_bcyan = 96
    _fcolor_bwhite = 97
    _fcolor_reset = 39

    _bcolor_black = 40
    _bcolor_red = 41
    _bcolor_green = 42
    _bcolor_yellow = 43
    _bcolor_blue = 44
    _bcolor_purple = 45
    _bcolor_cyan = 46
    _bcolor_white = 47
    _bcolor_gray = 100
    _bcolor_bred = 101
    _bcolor_bgreen = 102
    _bcolor_byellow = 103
    _bcolor_bblue = 104
    _bcolor_bpurple = 105
    _bcolor_bcyan = 106
    _bcolor_bwhite = 107
    _bcolor_reset = 49

    _sequence_s = _esc + '%dm'
    _sequence_f = _esc + '%d;%dm'
    _sequence = _esc + '%d;%d;%dm'

    bold = _sequence_s % _style_bold

    black = _sequence_f % (_style_no, _fcolor_black)
    red = _sequence_f % (_style_no, _fcolor_red)
    green = _sequence_f % (_style_no, _fcolor_green)
    yellow = _sequence_f % (_style_no, _fcolor_yellow)

    default = _sequence_f % (_style_no, _fcolor_reset)
