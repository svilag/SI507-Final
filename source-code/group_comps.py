import parse_wgi

COMP_FP = './data/competitions.json'
GROUP_FP = './data/groups.json'

COMPS = parse_wgi.read_json(COMP_FP)
GROUPS = parse_wgi.read_json(GROUP_FP)

for group in GROUPS:
    g_name = group['name']
    for comp in COMPS:
        if g_name in comp['groups']:
            print(comp['title'])