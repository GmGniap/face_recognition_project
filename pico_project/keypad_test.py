from components.keypad import Keypad

keypad = Keypad(
    4, 4, 
    [8, 9, 10, 11, 12, 13, 14, 15],
    [['1','2',"3",'A'],['4','5','6','B'],['7','8','9','C'], ['*','0',"#","D"]]
    # [['1', '4', '7', "*"], ['2', '5', '8', '0'], ['3', '6', '9', '#'], ['A', 'B', 'C', 'D']]       
    )

def check_pwd():
    correct_pwd = '12345'
    enter_key = keypad.get_5digits_pwd()

    if correct_pwd == enter_key:
        print("You entered correct password!")
    else:
        print(f"You entered wrong password : {enter_key}")
        print("Please try again to enter: ")
        check_pwd()

if __name__ == "__main__":
    check_pwd()
    
"""
while True:
    if key := keypad.get_5digits_pwd():
        all_keys += key
        if len(all_keys) == 5:
            break
print(f"Enter : {all_keys}")
"""