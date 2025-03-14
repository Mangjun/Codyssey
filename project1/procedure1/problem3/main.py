import csv

data = list()

try :
    f = open('Mars_Base_Inventory_List.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)
    
    new_file = open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(new_file)

    for row in reader :
        print(row[0], row[1], row[2], row[3], row[4])
        data.append((row[0], row[1], row[2], row[3], row[4]))

    print()

    sort_list = sorted(data[1:], key=lambda x: x[4], reverse=True)
    sort_list.insert(0, data[0])
    
    for row in sort_list :
        if row[4] >= '0.7' :
            print(row[0], row[1], row[2], row[3], row[4])

    writer.writerows(sort_list)

    f.close()
    new_file.close()
except FileNotFoundError :
    print("File not found")