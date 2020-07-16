import copy

def context_buttons(columns_add, columns_remove, default):
    '''Define the columns possible for the add button, the default values are all the columns
    columns_per_action: List (columns passed by the add button)
    default: List (columns of the table)'''

    if columns_add is not None:
        #Define the values in the add button with the columns_add
        data_add = copy.deepcopy(default)
        for col in columns_add:
            if col in default:
                data_add.remove(col)

        #Looking the possible columns to remove, redefine the values for each button, Actualize columns of columns_add and columns_remove
        if columns_remove is not None:
            data_remove = columns_add

            for col in columns_remove:
                if col not in data_add:
                    data_add.append(col)
                    data_remove.remove(col) 
                    columns_remove.remove(col)
        else:
            #if dont exist columns_remove then the possible values to erase are the values added 
            data_remove = columns_add

    else:
        #By default all the columns are possible values to add
        data_add = default
        data_remove = []

    
    data_add.sort()
    data_remove.sort()

    return data_add, data_remove, columns_add, columns_remove



