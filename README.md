# Ecliptica Interpreter

**Disclaimer:**  
_This interpreter is still in development and may contain bugs please report any bugs you found._

### Proof of Turing Completeness
any bf code can be translated to Ecliptica using `bf-to-ec.py` BUT ecliptica uses 64 bit signed integers so any bf program cant work unless it written to be compatible with that  

### Commands
- **`0-9`**: Any number written will be set to the current cell.
- **`''`**: Any char written inside '' will set to the current cell not as string as ascii value.
- **`/ /`**: / / considered comment comments must be inside /comment/ also comments are making code readable but in exchange slows the code by a fucking lot if you use comment inside a loop 
- **`>`**: Move the memory pointer to the right (increment the pointer).
- **`<`**: Move the memory pointer to the left (decrement the pointer).
- **`+`**: Increment the value at the current memory pointer.
- **`-`**: Decrement the value at the current memory pointer.
- **`O`**: Output the value at the current memory pointer as a character.
- **`o`**: Output the value at the current memory pointer as a number.
- **`?`**: Conditional check. If the value at the current memory pointer does not equal the next token (an integer), skip to the next `)`.
- **`[`**: Start a loop. Push the current program counter onto the stack.
- **`]`**: End a loop. Return to the beginning of the loop if the value at the current memory pointer is not zero.
- **`p`**: Copy the value at the pointer to another memory location (specified by the next token).
- **`P`**: Copy the value from another memory location (specified by the next token) to the pointer.
- **`n`**: Normalize the value at the pointer (set to `0` if negative, `1` if non-negative).
- **`i`**: Take user input and store it in the memory as ASCII values.
- **`x`**: Exit the program.
- **`t`**: Exit a loop prematurely (break out of nested loops).
- **`l`**: Store the length of the input stack at the current memory location.
- **`r`**: Perform a random operation by comparing two random numbers. If the first is larger, increase the value at the pointer. If not, decrease it.

### Control Flow
- Loops are enclosed between `[` and `]`. If the value at the pointer is zero when reaching `]`, the program skips back to `[`.
- The `?` token allows conditional execution, skipping to the next `)` if the condition is not met.
- 
### Input/Output
- The `i` command allows the user to input a string, which is converted into ASCII values and stored in memory.
- The `O` and `o` commands output the value at the memory pointer, either as a character or a number, respectively.


### Todo
 - optimize the code performance is awfull


pypy is recommended because interpreter is  slow


also i made an ecliptica to c compiler but its dogshit i wouldnt recommend it but works i guess except for comments dont use comments when compiling
also this is a valid code in it 
0?0(]
   
