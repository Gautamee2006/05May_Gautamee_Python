#Given the following buggy code, fix it so that it catches both IndexError and KeyError and prints
# a custom message for each:<br><br>
#my_list = [1, 2, 3]
#print(my_list[5])
#my_dict = {'a': 1}
#print(my_dict['b'])<br><br><em><strong>Hint:</strong> Use multiple except clauses to handle
# each exception separately.</em>

try:
    my_list = [1, 2, 3]
    print(my_list[5])

except IndexError:
    print("List index does not exist!")

try:
    my_dict = {'a': 1}
    print(my_dict['b'])

except KeyError:
    print("Dictionary key not found!")