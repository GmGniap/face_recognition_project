from machine import Pin
from utime import sleep

class Keypad:

    def __init__(self, row_size, column_size, pin_list, keys):
        """
        row_size: write the row number of the keypad.
        column_size : write the column number of the keypad.
        pin_list: write all the pins that will be used in a list.
        keys: write all keys in nested format. Example: keys = [['1','2',"3",'A'],['4','5','6','B'],['7','8','9','C'], ['*','0',"#","D"]]

        """
        self.__row_size = row_size
        self.__column_size = column_size
        self.__pin_list = pin_list
        self.__keys = keys

        self.__rows = pin_list[:row_size]
        self.__cols = pin_list[row_size:]

        self.__button = None
        self.__row_pins = []
        self.__col_pins = []

        self.__password = '55555'
        
        for pin_name in self.__rows:
            self.__row_pins.append(Pin(pin_name, Pin.OUT))

        for pin_name in self.__cols:
            self.__col_pins.append(Pin(pin_name, Pin.IN, pull=Pin.PULL_DOWN))

    def get_size(self):
        return self.__size

    def get_pin_list(self):
        return self.__pin_list

    def get_keys_list(self):
        return self.__keys

    def set_size(self, size):
        self.__size = size
        return self.__size

    def set_pin_list(self, pin_list):
        self.__pin_list = pin_list
        return self.__pin_list

    def set_key_list(self, keys):
        self.__keys = keys
        return self.__keys

    def scan(self, row, col):
        # set the current row to high, enable us to scan that row then check input columns
        self.__row_pins[row].value(1)
        key = None

        # checking for key pressed events
        if self.__col_pins[col].value() == 1:
            key = 1
        elif self.__col_pins[col].value() == 0:
            key = 0
        # after scanning set the row to zero
        self.__row_pins[row].value(0)

        return key

    def print_key_pressed(self):
        """
        This function prints the button that pressed on the keypad.
        """
        # first set all rows to low state
        for row in range(0, self.__row_size):
            self.__row_pins[row].value(0)

        while True:
            for row in range(0, self.__row_size):
                for col in range(0, self.__column_size):
                    key = self.scan(row, col)
                    if key == 1:
                        print("Key Pressed", self.__keys[row][col])
                        key = 0
                        sleep(0.3)
    
    def get_5digits_pwd(self):
        enter_key = ''
        # first set all rows to low state
        for row in range(self.__row_size):
            self.__row_pins[row].value(0)

        while True:
            if len(enter_key) == 5:
                return enter_key
            for row in range(self.__row_size):
                for col in range(self.__column_size):
                    key = self.scan(row, col)
                    if key == 1:
                        pressed_key = self.__keys[row][col]
                        print("Key Pressed: ", pressed_key)
                        enter_key += pressed_key
                        key = 0
                        sleep(0.3)
                        # if len(pressed_key) == 1:
                        #    return pressed_key
    
    def check_pwd(self):
        enter_key = self.get_5digits_pwd()

        if self.__password == enter_key:
            print("You entered correct password!")
            return True
        else:
            print(f"You entered wrong password : {enter_key}")
            print("Please try again to enter: ")
            self.check_pwd()

    def hex_integer_key_pressed(self):
        """
        Gives the integer value of the button, which has been pressed.
        Default A,B,C,D,*,# is assigned to 10,11,12,13,14,15. If you don't have these buttons you can change the code.
        """
        for row in range(0, self.__row_size):
            self.__row_pins[row].value(0)

            while True:
                for row in range(0, self.__row_size):
                    for col in range(0, self.__column_size):
                        key = self.scan(row, col)
                        if key == 1:
                            self.__button = self.__keys[row][col]
                            if self.__button == "A":
                                self.__button = 10
                            elif self.__button == "B":
                                self.__button = 11
                            elif self.__button == "C":
                                self.__button = 12
                            elif self.__button == "D":
                                self.__button = 13
                            elif self.__button == "*":
                                self.__button = 14
                            elif self.__button == "#":
                                self.__button = 15
                            else:
                                self.__button = int(self.__button)
                            key = 0
                            sleep(0.3)
                if self.__button is not None:
                    break

        return self.__button