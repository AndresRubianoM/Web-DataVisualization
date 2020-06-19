import os 
import json
import openpyxl


class Transform:
    def __init__(self, filename, route = None):
        self.file = filename
        self.route = route
        self.extension = self.file.split('.')[-1]
        self._path = self._absolute_path()
        self.list_values = self._proceed()
        
    def list_from_csv(self):
        rows_list = []
        path = self._absolute_path()
        with open(self._path, 'r') as file:
            data = file.readlines()
            for line in data:
                rows_list.append(line.split(','))
        return rows_list
    
    def list_from_xlsx(self):
        file = openpyxl.load_workbook(self._path)
        sheet = file.active
        rows_list = []

        for row in sheet.iter_rows(max_row = sheet.max_row):
            cells_rows = []
            for cell in row:
                cells_rows.append(cell.value)
            rows_list.append(cells_rows)
        
        return rows_list
    
    def list_from_json(self):
        rows_list = []
        with open(self._path, 'r') as file:
            data = json.load(file)
            rows_list.append(list(data[1].keys()))
            for line in data:
                rows_list.append(list(line.values()))
            
        return rows_list

    def _proceed(self):
        '''Select the procedure to each of the valid extensions'''
        if self.extension == 'csv':
            return self.list_from_csv()
        elif self.extension == 'xlsx':
            return  self.list_from_xlsx()
        elif self.extension == 'json':
            return  self.list_from_json()
        else:
            return None

        

                       
    def _absolute_path(self):
        '''Define the absolute path to de file'''
        if self.route is not None:
            #Asolute path to the current script
            my_path = os.path.abspath(os.path.dirname(__file__))
            path_relative_file = os.path.join(self.route ,  self.file)
            #Absolute path to the data file
            path = os.path.join(my_path, path_relative_file)
            return path
        else:
            return None


    


if __name__ == "__main__":
    route = r'..\_uploads'
    file =  'mtcarsjson.json'

    my_path = os.path.abspath(os.path.dirname(__file__))
    path_relative_file = os.path.join(route ,  file)
    #Absolute path to the data file
    path = os.path.join(my_path, path_relative_file)

    words = Transform(file, route)
    print(words.list_from_json())
    '''#
    rows_list = []
    with open(path, 'r') as file:
        data = json.load(file)
        print(list(data[1].keys()))
        rows_list.append(list(data[1].keys()))
        for line in data:
            rows_list.append(list(line.values()))
            
        print(rows_list)'''






    """ rows_list = []
    


    file = openpyxl.load_workbook(path)
    sheet = file.active
    #print(sheet)
    #print(sheet.max_row, sheet.max_column)
    for row in sheet.iter_rows(max_row = sheet.max_row):
        cells_sheet = []
        for cell in row:
            cells_sheet.append(cell.value)
        rows_list.append(cells_sheet)
        #print(rows_list) """
        


    """ import os 
    #Asolute path to the current script
    my_path = os.path.abspath(os.path.dirname(__file__))
    #Absolute path to the data file
    path = os.path.join(my_path, r'..\_uploads\mtcars.csv')
    
    var = []

    with open(path, 'r') as file:
        data = file.readlines()
        for line in data:
            var.append(line.split(',')) """
            

        
