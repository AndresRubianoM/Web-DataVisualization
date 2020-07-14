import copy

def context_buttons(columns_per_action, default):
    '''Define the columns possible for the add button, the default values are all the columns
    columns_per_action: List (columns passed by the add button)
    default: List (columns of the table)'''

    if columns_per_action is not None:
        data_add = copy.deepcopy(default)
        for col in columns_per_action:
            if col in default:
                data_add.remove(col)

        data_remove = columns_per_action
    else:
        data_add = default
        data_remove = []

    return data_add, data_remove



