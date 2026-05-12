def buildUnorderedList(details):
    line = []
    for key, val in details.items():
        color = 'green'
        if val == None or val == "no" or val == "No":
            color = 'red'

        line.append(f"<li>{key} : <span style='color:{color}'>{val}</span></li>")

    return line    