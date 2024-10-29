def translate(code):
    chars = {
        '+': '+',
        '-': '-',
        '<': '<',
        '>': '>',
        '[': '[?0(t)',
        ']': ']',
        '.': 'O',
        ',': 'i'
    }

    custom_code = ''.join(chars[char] for char in code if char in chars)

    return custom_code

if __name__ == "__main__":
    brainfuck_input = """
    code here
    """
    translated_code = translate(brainfuck_input)
    print(translated_code)  
    # NOTE! ecliptica works with negative numbers and each cell is 64 bit that means not any program will work in it 
