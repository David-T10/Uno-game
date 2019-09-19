#MVC example inventory using C.R.U.D- Create Read Update Delete
import mvc_exceptions as mvc_exc

items = list()

def create_item(name, price, quantity):
    global items
    results = list(filter(lambda x: x['name'] == name, items))
    if results:
        raise mvc_exc.ItemAlreadyStored('"{}" already stored!'.format(name))
    else:
        items.append({'name': name, 'price': price, 'quantity': quantity})
#mvc_exc checks if item has already been stored and if so passes the class ItemAlreadyStored
def create_items(add_items):
    global items
    items = app_items
    
def read_item(name):
    global items
    myitems = list(filter(lambda x: x['name'] == name, items))
    if myitems:
        return myitems[0]
    else:
        raise mvc_exc.ItemNotStored('"{}" does not exist'.format(name))

def read_items():
    global items
    return [item for item in items]

def update_item(name, price, quantity):
    global items
    idxs_items = list(filter(lamba i_x: i_x[1]['name'] == name, enumerate(items)))
