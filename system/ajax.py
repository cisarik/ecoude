from models import Shellserver

htmlCodes = [
             ['"', '\''],
             ['!', '"'],
             ['\n', ' '],
             ]
htmlCodesReversed = htmlCodes[:]
htmlCodesReversed.reverse()

def htmlDecode(s, codes=htmlCodesReversed):
    """ Returns the ASCII decoded version of the given HTML string. This does
        NOT remove normal HTML tags like <p>. It is the inverse of htmlEncode()."""
    for code in codes:
        s = s.replace(code[1], code[0])
    return s

def htmlEncode(s, codes=htmlCodes):
    """ Returns the HTML encoded version of the given string. This is useful to
        display a plain ASCII text string on a web page."""
    for code in codes:
        s = s.replace(code[0], code[1])
    return s

def admin_shellserver_refresh():
    return {'shellservers':Shellserver.objects.all()}