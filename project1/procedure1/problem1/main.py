print('Hello Mars')

try :
    f = open('mission_computer_main.log', 'r')
    lines = f.readlines()
    print(lines[0], end='')
    for line in reversed(lines[1:]) :
        print(line, end='')
    f.close()
except FileNotFoundError :
    print('File not found')