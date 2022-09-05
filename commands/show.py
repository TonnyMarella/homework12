def show(command, adressbook):
    if command == 'show all':  # Show all contacts
        print(adressbook.data)
    elif command == 'show':  # Show one contact
        name = input('Enter name:\n')
        if adressbook.is_data(name):
            print('name:', adressbook.data[name].name.value, 'phone:',
                  list(map(lambda x: x.value, adressbook.data[name].phones)))
        else:
            print('Enter correct name')
    elif command == 'show_iter':
        count = int(input('Enter the number of entries:\n'))
        generator = adressbook.iterator()
        for i in range(count):
            try:
                print(next(generator))
            except StopIteration:
                print('No more contacts')
