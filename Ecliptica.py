import re
import sys
import random
class EclipticaInterpreter:
    def __init__(self):
        self.memory = []
        self.ptr = 0  
        self.program_counter = 0
        self.stack = []  
        self.input_stack = []  
        self.tokens = []
        self.running = True

    def initialize_memory(self, size):
        self.memory = [0] * size

    def error(self, message):
        raise Exception(f"Error: {message}")

    def tokenize(self, code):
        # Match integers, commands, and operators
        token_pattern = re.compile(r"([0-9]+|[<>+\-Oo\?\[\]bntx'c()]|.)")
        tokens = re.findall(token_pattern, code)
        return tokens

    def run(self, code):
        self.tokens = self.tokenize(code)
        self.program_counter = 0
        while self.program_counter < len(self.tokens) and self.running:
            token = self.tokens[self.program_counter]
            self.process_token(token)
            self.program_counter += 1

    def process_token(self, token):
        if re.match(r'^[0-9]+$', token):
            value = int(token)
            self.memory[self.ptr] = value
        elif token == ">":
            self.ptr += 1
        elif token == "<":
            self.ptr -= 1
        elif token == "p":
            self.program_counter += 1 
            index_to_copy = int(self.tokens[self.program_counter])   
            self.memory[index_to_copy] = self.memory[self.ptr]  
        elif token == "P":
            self.program_counter += 1 
            index_to_copy = int(self.tokens[self.program_counter])   
            self.memory[self.ptr] = self.memory[index_to_copy]                      
        elif token == "+":
            self.memory[self.ptr] = (self.memory[self.ptr] + 1) & ((1 << 64) - 1)  # 64-bit signed
        elif token == "-":
            self.memory[self.ptr] = (self.memory[self.ptr] - 1) & ((1 << 64) - 1)
        elif token == "O":

            sys.stdout.write(chr(self.memory[self.ptr]))
            sys.stdout.flush()
        elif token == "o":
            sys.stdout.write(str(self.memory[self.ptr]))
            sys.stdout.flush()
        elif token == "'":
            # Expect the next token to be a character
            self.program_counter += 1
            char_token = self.tokens[self.program_counter]
            self.program_counter += 1 
            if self.tokens[self.program_counter] != '\'': self.error("' is not closed tokens caused error: " + '\'' + char_token + self.tokens[self.program_counter])
            else:
                self.memory[self.ptr] = ord(char_token)
        elif token == "?":
            self.program_counter += 1  
            condition_value = int(self.tokens[self.program_counter])  #
            if self.memory[self.ptr] != condition_value:
                while self.tokens[self.program_counter] != ")":
                    self.program_counter += 1
        elif token == "[":
            self.stack.append(self.program_counter)
        elif token == "]":
            start_loop = self.stack.pop()
            self.program_counter = start_loop - 1  
        elif token == "n":
            if self.memory[self.ptr] < 0:
                
                self.memory[self.ptr] = 0
            else:  self.memory[self.ptr] = 1    
        elif token == "i":
            if not self.input_stack:
                user_input = input()
                self.input_stack = list(reversed([ord(c) for c in user_input]))
            if self.input_stack:
                self.memory[self.ptr] = self.input_stack.pop()
        elif token == "x":
            self.running = False
        elif token == "/":
            self.program_counter += 1
            while True:
                if self.tokens[self.program_counter] == "/": break
                self.program_counter += 1

        elif token == "t":
            self.tstack = []
            while  True:
                if self.program_counter >= len(self.tokens): raise IndexError("program counter is bigger than tokens perhabs you forgot ] while stopping a loop ?")
                elif self.tokens[self.program_counter] == "]":
                    if len(self.tstack) > 0:
                        self.tstack.pop()
                    else:
                        self.stack.pop()
                        break
                elif self.tokens[self.program_counter] == "[":self.tstack.append(1)        
                self.program_counter += 1
 
        elif token == " ": pass
        elif token == "\n": pass
        elif token == "l": 
            self.memory[self.ptr] = len(self.input_stack)
        elif token == "r":
           a = random.randint(-10, 20)
           b = random.randint(-10, 20)
           if a > b:
            self.memory[self.ptr] += random.randint(1, 5)  
           else:  self.memory[self.ptr] -= random.randint(1, 5)              
        elif token == ")": pass
        elif token == "(":pass
        else:
            self.error(f"Unknown token: {token}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Ecliptica.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        code = file.read()  
    interpreter = EclipticaInterpreter()
    interpreter.initialize_memory(65535)
    interpreter.run(code)
