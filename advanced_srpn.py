
# This is your SRPN file. Make your changes here.
class MainSrpn:
    """ The main class in which all methods for necessary formats
    and calculations are called from """
    def __init__(self):
        #flags for if it is currenlty in a comment of the stack is full
        self.current_comment = False
        self.stack_overflow = False

        #the main stack commands are passed into/popped from
        self.cmd_stack = []

        #the list of pseudo random numbers
        self.r_nums = [
            '1804289383', '846930886', '1681692777', '1714636915',
            '1957747793', '424238335', '719885386', '1649760492', '596516649',
            '1189641421', '1025202362', '1350490027', '783368690',
            '1102520059', '2044897763', '1967513926', '1365180540',
            '1540383426', '304089172', '1303455736', '35005211', '521595368',
            '1804289383', '846930886', '1681692777'
        ]
        self.r_index = 0

    def check_stack_length(self):
        """checks the length of the stack and returns
        true if no more elements can be added"""

        if len(self.cmd_stack) > 22:
            self.stack_overflow = True

    def display_stack(self):
        """ Displays the current stack """
        for n in self.cmd_stack:
            print(n)

    def check_negitive_number(self, command, index):
        """Checks if a - sign is the start of a negative number"""
        if len(command)>index+1 and command[index+1].isdigit():
            if index>0 and command[index-1].isdigit():
                #if the character before is a number, it should be treated as an operator, not the start of a negative number
                return False
            return True
        return False

    def number_length(self, number, index):
        """ Gives the number of continuous digits in a string """
        temp_index = index
        while temp_index < len(number):
            if number[temp_index].isdigit():
                temp_index += 1
            else:
                break
        return temp_index - index

    def format_number(self, number, index, length):
        """ Converts a string of given length of digits
         into an integer """
        n = number[index:index + length]

        if number[index]=="0":
            #if the number starts with 0 and is an octal number it is converted, otherwise it is passed
            nums_allowed=["0","1","2","3","4","5","6","7"]
            matched_list = [characters in nums_allowed for characters in n]
            if all(matched_list):
                return int(n,8)
            else:
                return False
        else:
            return int(n)

    def calculate(self, operator):
        """The main function for calculating the results when
        given a valid operator"""

        a = int(self.cmd_stack[-2])
        b = int(self.cmd_stack[-1])

        max_value = 2147483647
        min_value = -2147483648
        value = 0

        if operator == "+":
            value = a + b

        elif operator == "-":
            value = a - b

        elif operator == "/":
            if b != 0:
                #makes sure number is rounded down
                a=a-a%b
                value = int(a/b)
                min_value = -2147483647
            else:
                print("Divide by 0.")
                return
        elif operator == "*":
            value = a * b
        elif operator == "%":
            value = a % b
        elif operator == "^":
            if b < 0:
                print("Negative power.")
                return
            value = a**b

        if min_value < value < max_value:
            self.cmd_stack.append(value)

        elif value >= max_value:
            self.cmd_stack.append(max_value)

        elif value <= min_value:
            self.cmd_stack.append(min_value)

        self.cmd_stack.pop(-2)
        self.cmd_stack.pop(-2)

    def take_input(self, command):
        """The function which takes the initial input,
         formats it or does a calculation depending on
         what the input is"""
        index = 0
        while index < len(command):
            c = command[index]
            if self.current_comment:
                if c == "#":
                    self.current_comment = False
            else:
                if c == "#":
                    self.current_comment = True
                elif c.isdigit():
                    
                    self.check_stack_length()
                    num_len = self.number_length(command, index)
                    if not self.stack_overflow:
                        new_num = self.format_number(command, index, num_len)
                        if new_num:
                            new_num = min(new_num, 2147483647)

                            self.cmd_stack.append(new_num)
                    else:
                        print("Stack overflow.")

                    index += num_len - 1
                elif c == "-" and self.check_negitive_number(command,index):
                    self.check_stack_length()
                    num_len = self.number_length(command, index + 1)
                    if not self.stack_overflow:
                        new_num = self.format_number(command, index + 1,
                                                     num_len)
                        if new_num:
                            if new_num > 2147483647:
                                new_num = 2147483648
                            self.cmd_stack.append(0 - new_num)
                    else:
                        print("Stack overflow.")
                    index += num_len

                elif c in {'+', '-', '/', '*', '%', '^'}:

                    if index<len(command)-1 and command[index+1]=="=":
                        #accounts for cases where there is no space before =
                        print(self.cmd_stack[-1])
                        index+=1

                    if len(self.cmd_stack) < 2:
                        print("Stack underflow.")

                    else:
                        self.calculate(c)

                elif c == "r":
                    self.check_stack_length()

                    if not self.stack_overflow:
                        self.cmd_stack.append(self.r_nums[self.r_index])
                        self.r_index += 1
                    else:
                        print("Stack overflow.")

                elif c == "d":
                    self.display_stack()
                elif c == " ":
                    pass
                elif c == "=":
                    print(self.cmd_stack[-1])
                else:
                    print(f'Unrecognised operator or operand "{c}".')

            index += 1


# makes an instance of the main class
main_SRPN = MainSrpn()


def process_command(command):
    """passes the input to the main instance of the class"""
    main_SRPN.take_input(command)


#This is the entry point for the program.
#Do not edit the below
if __name__ == "__main__":
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
            if pc != None:
                print(str(pc))
        except:
            exit()
