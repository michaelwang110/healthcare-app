# check if search matches target sufficiently
def match(target, search):
    target = target.lower()
    search = search.lower()
    # remove space if first character in search
    if search[0] == " ":
        search = search[1:]
    # GP case
    if target == "gp":
        if search in target:
            return True
        else:
            target = "general practitioner doctor"
    # ignore single character searches
    if len(search) == 1:
        return False
    #general case
    if search in target:
        return True
    elif len(search) > len(target):
        if search[:len(target)] in target:
            return True
    elif len(search) > 3:
        if search[:3] in target:
            return True
    return False
