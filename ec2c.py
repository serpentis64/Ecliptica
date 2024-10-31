import re

def tokenize(ecliptica_code):
    tokens = []
    i = 0
    length = len(ecliptica_code)

    while i < length:
        char = ecliptica_code[i]

        if char.isspace():
            i += 1
            continue

    
        if char == '/' and i + 1 < length and ecliptica_code[i + 1] == '/':
            i = ecliptica_code.find('\n', i + 2)  
            if i == -1:  
                break
            continue

      
        if char.isdigit():
            number = ""
            while i < length and ecliptica_code[i].isdigit():
                number += ecliptica_code[i]
                i += 1
            tokens.append(number)
            continue

        if char == '\'':
            if i + 2 < length and ecliptica_code[i + 2] == '\'':
                tokens.append(ecliptica_code[i:i + 3])  
                i += 3
                continue
            else:
                raise ValueError("Malformed character literal")

        
        if char in ['>', '<', '+', '-', 'O', 'o', '?', '(', ')', '[', ']', 'p', 'P', 'n', 'i', 'x', 't', 'l', 'r']:
            tokens.append(char)
            i += 1
            continue

        raise ValueError(f"Unknown token: {char}")

    return tokens

def ec_to_c(code):
    tokens = tokenize(code)
    i = 0
    # this is written by ai i know no shit about c i am a py developer what u expect
    # also this whole shit almost driving me to crazy 
    # fuck c 
    # fuck ecliptica
    c_code = """ 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define MAX_INPUT_SIZE 8000

char input_buffer[MAX_INPUT_SIZE];
int input_length = 0;

void read_input() {
    int ch;
    input_length = 0;

    while (input_length < MAX_INPUT_SIZE - 1 && (ch = getchar()) != EOF) {
        if (ch == '\\n') {
            break;
        }
        input_buffer[input_length++] = (char)ch;
    }

    input_buffer[input_length] = '\\0'; // Null-terminate the string
}

int get_input_length() {
    return input_length-1;
}

int buffered_getchar() {
    static int index = 0;

    if (index < input_length) {
        return (unsigned char)input_buffer[index++];
    }
    
    // Reset index and read new input if buffer is empty
    index = 0;
    read_input();
    
    return buffered_getchar();
}



int main() {
    
    int ptr = 0;
    int ch;
    srand(time(NULL));
    int memory[65535] = {0};
"""

    while i < len(tokens):
        token = tokens[i]

        if token.isdigit():
            c_code += f"\n    memory[ptr] = {token};"
        elif token == "+":
            c_code += "\n    memory[ptr] += 1;"
        elif token[0] == "'":
            c_code += f"\n    memory[ptr] += {token};"            
        elif token == "-":
            c_code += "\n    memory[ptr] -= 1;"
        elif token == ">":
            c_code += "\n    ptr += 1;"
        elif token == "<":
            c_code += "\n    ptr -= 1;\n    " # if (ptr < 0) { printf(\"Error: ptr can't be negative\"); return 0; }
        elif token == "o":
            c_code += "\n    printf(\"%d\", memory[ptr]);"
        elif token == "O":
            c_code += "\n    printf(\"%c\", (char)memory[ptr]);"
        elif token == "?":
            i += 1
            if tokens[i].isdigit():
                c_code += f"\n    if (memory[ptr] == {tokens[i]})"
        elif token == "(":
            c_code += " {"
        elif token == ")":
            c_code += " }"
        elif token == "[":
            c_code += "\n    while (1) {"
        elif token == "]":
            c_code += " }"
        elif token == "t":
            c_code += "\n    break;"
        elif token == "x":
            c_code += "\n    return 0;"
        elif token == "p":
            i += 1
            if tokens[i].isdigit():
                c_code += f"\n    memory[{tokens[i]}] = memory[ptr];"
        elif token == "P":
            i += 1
            if tokens[i].isdigit():
                c_code += f"\n    memory[ptr] = memory[{tokens[i]}];"
        elif token == "l":
            c_code += "\n    memory[ptr] = get_input_length();"
        elif token == "i":
            c_code += """\n    ch = buffered_getchar();memory[ptr] = ch;"""
        elif token == "n":
            c_code += """\n    if(memory[ptr]<0){memory[ptr]=0;}else{memory[ptr]=1;}"""            
        i += 1

    c_code += "\n    return 0;\n}"

    return c_code
if __name__ == "__main__":
    import sys
    import os
    print("warning! this compiler made like shit dont use it its buggy as hell and code will not work %60 of the time atleast yapi works :D ")
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

   
    input_filename = sys.argv[1]


    with open(input_filename, 'r') as file:
        content = file.read()

    
    processed_content = ec_to_c(content)

 
    output_filename = os.path.splitext(input_filename)[0] + ".c"


    with open(output_filename, 'w') as file:
        file.write(processed_content)

    print(f"code compiled {output_filename}")
