import random

def generation()->list:
    def check_validity(x,y,number):

        #main check
        def checkcoordslist(coordslist:list)->bool:
            for coords in coordslist:
                #print(coordslist)
                try:
                    test(field)
                    if field[coords[1]][coords[0]] == number:
                        print("war hier")
                        return False
                        
                except IndexError:
                    print("index error jajajaja")
            print("das ist ein ja")        
            return True
        
        def check_row():
            coordslist = []
            for i in range(0,x):
                coordslist.append([i,y])
            print("row gecheckt")
            return checkcoordslist(coordslist=coordslist)
            
        def check_column():
            coordslist = []
            for i in range(0,y):
                coordslist.append([x,i])
            print("column gecheckt")
            return checkcoordslist(coordslist=coordslist)
        def check_area():
            #detect area
            return True
        
         
        if check_area() and check_column() and check_row():
            return True
        else:
            return False
        
    #basic field filled with 0s
    field = []
    for y in range(0,9):
        row = []
        for x in range(0,9):
            row.append(0)
        field.append(row)

    #assignment of actual numbers
    for row in field:
        for column in row:
            y = field.index(row)
            x = row.index(column)
            trigger = False
            while not trigger:
                number = random.randint(1,9)
                if check_validity(x,y,number):
                    field[y][x] = number
                    test(field)
                    trigger = True
                    

def test(array:list):
    for i in array:
        print(i)

    print("------------------------------------------")

if __name__ == "__main__":
    test(generation())