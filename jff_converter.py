import xmltodict


def convert(filename):
    data = open(filename, 'r')
    xml_content = data.read()
    data.close()

    xml_dict = xmltodict.parse(xml_content)
    new_dict = {
        "Q": [],
        "Sigma": [],  # note that it's impossible to determine "Sigma" and "Gamma" with the data store in a .jff file
        "Gamma": [],
        "Delta": {},
        "B": "#",
        "q0": "",
        "F": []
    }

    # .jff files may have a list of <state> or a list of <block> to represent states.
    # Both use an "id" attribute, so we only care about the name of the tags.
    try:
        xml_dict['structure']['automaton']['state'] = xml_dict['structure']['automaton']['state']
        key_name = 'state'
    except KeyError:
        key_name = 'block'

    # Go through states and fill "Q", "q0" and "F"
    for s in xml_dict['structure']['automaton'][key_name]:
        new_dict["Q"].append("q" + s['@id'])  # "@name" is irrelevant in the list of transitions, so we use "@id"
        if 'initial' in s:
            new_dict["q0"] = "q" + s['@id']
        if 'final' in s:
            new_dict["F"].append("q" + s['@id'])
    # Add states to "Delta"
    for s in new_dict["Q"]:
        new_dict["Delta"][s] = {}
    # Go through transitions and fill "Delta" states (mostly notation considerations)
    for t in xml_dict['structure']['automaton']['transition']:
        state = "q" + t['from']
        if t['read'] is None:
            r = "#"
        else:
            r = t['read']

        if t['write'] is None:
            e = "#"
        else:
            e = t['write']

        m = t['move'].lower()
        q = "q" + t['to']

        new_dict["Delta"][state][r] = {"q": q, "e": e, "m": m}

    return new_dict
