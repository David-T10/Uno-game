#MVC example inventory using C.R.U.D- Create Read Update Delete
#basic_backend forms the basis of the MODEL in MVC (creating basic funtions required)
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
def create_items(app_items):
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
    idxs_items = list(filter(lambda i_x: i_x[1]['name'] == name, enumerate(items)))
    if idxs_items:
        i, item_to_update = idxs_items[0][0], idxs_items[0][1]
        items[i] = {'name': name, 'price': price, 'quantity': quantity}
    else:
        raise mvc_exc.ItemNotStored('Can not update "{}" because it is not stored'.format(name))
def delete_item(name):
    global items
    idxs_items = list(filter(lambda i_x: i_x[1]['name'] == name, enumerate(items)))
    if idxs_items:
        i, item_to_delete = idxs_items[0][0], idxs_items[0][1]
        del items[i]
    else:
        raise mvc_exc.ItemNotStored('Can not update "{}" because it is not stored'.format(name))

'''def main():

    my_items = [{'name': 'bread', 'price': 0.5, 'quantity': 20},
                {'name': 'milk', 'price': 1.0, 'quantity': 10},
                {'name': 'wine', 'price': 10.0, 'quantity': 5},]

    create_items(my_items)
    #create_item('bread', price=3.0, quantity=15)
    #testing ItemAlreadyStored exception

    #reading items in my_items
    print('Stored Items are:')
    print(read_items())

    update_item('bread', 2.0, 10)
    print(read_items())
    

if __name__=='__main__':
    main()'''
