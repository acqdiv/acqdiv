# get all the text contained in an XML tag. This is useful for mixed elements of the form <t1>a<t2>b</t2>c<t1>
def content(tag):
    return tag.text + ''.join(ET.tostring(e) for e in tag)

# create a new key/value pair in a dictionary or concatenate an additional value if the key already exists
def creadd(location, key, value):
    if key not in location.keys():
        location[key] = value
    else:
        location[key] += '; ' + value

# increment an index and extend list nested in Vividict accordingly
def list_index_up(index, vivilist):
    # count up index
    index += 1
    # check if list in Vividict is too short for present index
    if len(vivilist) <= index:
        # if it is, append empty element to list to extend index
        vivilist.append(Vividict())
    return index

# extend list nested in Vividict if it is to short for a counter variable
def ext_vivi(index, vivilist):
    # check if list in Vividict is too short for present index
    if len(vivilist) <= index:
        # if it is, append empty element to list to extend index
        vivilist.append(Vividict())
