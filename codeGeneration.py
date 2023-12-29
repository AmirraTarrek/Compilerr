# Code Generation 

class Register_Allocator:
    count = 0
    dictionary = {}

    def registerAllocation(obj, var):
        if var not in obj.dictionary:
            obj.count += 1
            obj.dictionary[var] = f"R{obj.count}"  #R1-R2-R3-R4-R5

        return obj.dictionary[var]

allocator = Register_Allocator()

##############################################################################

class TargetGenerator:
    @staticmethod
    def load(x, y):
        return f"LDR {x}, {y}"

    @staticmethod
    def add(x, y):
        return f"ADD {x}, {y}"

    @staticmethod
    def mul(x, y):
        return f"MUL {x}, {y}"
    
    @staticmethod
    def store(x, y):
        return f"STR {x}, {y}"

generator = TargetGenerator()

##############################################################################

def codeGeneration (input, allocator, generator):
    target = []

    tokens = input[0].split()

    if len(tokens) == 7 and tokens[1] == "=": #I = J * K + L
        r1 = allocator.registerAllocation(tokens[0])
        r2 = allocator.registerAllocation(tokens[2])
        r3 = allocator.registerAllocation(tokens[4])
        r4 = allocator.registerAllocation(tokens[6])

        target.append(generator.load(r2, tokens[2]))
        target.append(generator.load(r3, tokens[4]))
        target.append(generator.mul(r3, r2))
        target.append(generator.load(r4, tokens[6]))
        target.append(generator.add(r4, r3))
        target.append(generator.store(r4, tokens[0]))

    else:
        print("Invalid")

    return target

##############################################################################

input = ["I = J * K + L"]
target = codeGeneration(input, allocator, generator)

########################

print("Input Code:")
for x in input:
    print(x)

print("\nTarget Code:")
for x in target:
    print(x)
