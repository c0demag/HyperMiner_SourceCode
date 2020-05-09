declared = {}
naming_dict = {}
declarations = []
out_counter = 0
rules = []
counter=-1
length=1
TraceEnds = []
magic_transform = set()
def init(trs):
    global declared, declarations, rules, counter, length, TraceEnds, naming_dict, out_counter, magic_transform
    declared = {}
    declarations = []
    rules = []
    counter=-1
    length=1
    if trs == []:
        TraceEnds = []
    naming_dict = {}
    out_counter = 0
    magic_transform = set()
