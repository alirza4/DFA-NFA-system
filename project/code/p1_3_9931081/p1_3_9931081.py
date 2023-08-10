class ObjectNFA:
    def __init__(self, status_set, alphabetstarget_set, transitions_set, start_set, final_set):
        #set status
        self.status = status_set
        #set alphabets
        self.alphabetstarget = alphabetstarget_set
        #dictionary transition functions
        self.transitions = transitions_set
        #set accept states
        self.start = start_set
        #set current state
        self.final = final_set

def nfa_concatenate(nfa1, nfa2):
    #Performs concatenation on two NFA && Create the alphabet array by combining the alphabets
    alphabetstarget = [alphabet for alphabet in nfa1.alphabetstarget]
    for l in nfa2.alphabetstarget:
        if l not in alphabetstarget:
            alphabetstarget.append(l)
    final = []
    transitions = []        
    status = []
    start = []
    #add status from first NFA && second NFA 
    for i in range(len(nfa1.status)):
        current_state = nfa1.status[i]
        status.append(current_state)
        if current_state in nfa1.start:
            start.append(current_state)       
    for i in range(len(nfa2.status)):
        current_state = nfa2.status[i]
        effective_state = "Q" + str(i + len(nfa1.status))
        status.append(effective_state)
        if current_state in nfa2.final:
            final.append(effective_state)
         #add transitions from first NFA && second NFA
        if current_state in nfa2.start:
            for nfa1_final_state in nfa1.final:
                transitions.append([nfa1_final_state, 'λ', effective_state])
    for arc in nfa1.transitions:
        transitions.append(arc)
    for arc in nfa2.transitions:
        [origin_state, input_letter, next_state] = arc
        n_origin_state = 'Q' + str(int(origin_state[1:]) + len(nfa1.status))
        n_next_state = 'Q' + str(int(next_state[1:]) + len(nfa1.status))
        transitions.append([n_origin_state, input_letter, n_next_state])

    return ObjectNFA(status, alphabetstarget, transitions, start, final)

def regex_to_nfa(alphabet):
    #Convert unit regular expression to NFA && Define the status, alphabets, final states,... 
    alphabetstarget = [alphabet]
    transitions = [
        ["Q0", alphabet, "Q1"],
    ]
    status = ["Q0", "Q1"]
    start = ["Q0"]
    final = ["Q1"]
    return ObjectNFA(status, alphabetstarget, transitions, start, final)


def combine_nfa(nfa1, nfa2):
    #Create array of alphabets,status by combining nfa1 and nfa2
    alphabetstarget = [alphabet for alphabet in nfa1.alphabetstarget]
    for l in nfa2.alphabetstarget:
        if l not in alphabetstarget:
            alphabetstarget.append(l)
    status = ["Q0"]
    start = ["Q0"]
    final = []
    transitions = []
    #add status and transition from nfa1 and nfa2
    for i in range(len(nfa1.status)):
        current_state = nfa1.status[i]
        effective_state = 'Q' + str(i + 1)
        status.append(effective_state)

        if current_state in nfa1.final:
            final.append(effective_state)
        if current_state in nfa1.start:
            transitions.append(['Q0', 'λ', effective_state])
    for i in range(len(nfa2.status)):
        current_state = nfa2.status[i]
        effective_state = "Q" + str(i + 1 + len(nfa1.status))
        status.append(effective_state)

        if current_state in nfa2.final:
            final.append(effective_state)
        if current_state in nfa2.start:
            transitions.append(['Q0', 'λ', effective_state])
    for arc in nfa1.transitions:
        [origin_state, input_letter, next_state] = arc
        n_origin_state = 'Q' + str(1 + int(origin_state[1:]))
        n_next_state = 'Q' + str(1 + int(next_state[1:]))
        transitions.append([n_origin_state, input_letter, n_next_state])

    for arc in nfa2.transitions:
        [origin_state, input_letter, next_state] = arc
        n_origin_state = 'Q' + str(1 + int(origin_state[1:]) + len(nfa1.status))
        n_next_state = 'Q' + str(1 + int(next_state[1:]) + len(nfa1.status))
        transitions.append([n_origin_state, input_letter, n_next_state])
    #return combined NFA
    return ObjectNFA(status, alphabetstarget, transitions, start, final)

def validate_alphabet(character):
    flag = False
    if (character >= '0') and (character <= '9'):
        flag = True
    elif (character >= 'a') and (character <= 'z'):
        flag = True 
    return flag


def add_dot(regex):
    #find indices && insert dots at the appropriate indices
    indic = []
    new_regex = regex[:]

    for i in range(len(regex) - 1):
        cc = regex[i]
        cn = regex[i + 1]
        if (cc == ')') or (cc == '*')or validate_alphabet(cc):
            if  cn == '(' or validate_alphabet(cn):
                indic.append(i)

    for i in range(len(indic)):
        index = indic[i]
        new_regex = new_regex[:index + i + 1] + "." + new_regex[index + i + 1:]

    return new_regex


def closure_nfa(nfa):
    #Create arrays for states, alphabets, start states,...
    #add transitions from base NFA
    
    status = ['Q0']
    for i in range(len(nfa.status)):
        effective_state = 'Q' + str(i + 1)
        status.append(effective_state)
    index = 1 + len(nfa.status)
    only_final_state = 'Q' + str(index)
    status.append(only_final_state)
    alphabetstarget = [letter for letter in nfa.alphabetstarget]
    start = ['Q0']
    final = [only_final_state]
    transitions = []
    for arc in nfa.transitions:
        [origin_state, input_letter, next_state] = arc
        n_origin_state = 'Q' + str(1 + int(origin_state[1:]))
        n_next_state = 'Q' + str(1 + int(next_state[1:]))
        transitions.append([n_origin_state, input_letter, n_next_state])
# Add lambda transitions from start states to other status and to the final status ,the final status to start status
    for st_state in nfa.start:
        transitions.append(['Q0', 'λ', 'Q' + str(1 + int(st_state[1:]))])
    transitions.append(['Q0', 'λ', only_final_state])

    for fn_state in nfa.final:
        transitions.append(['Q' + str(1 + int(fn_state[1:])), 'λ', only_final_state])
        for st_state in nfa.start:
            transitions.append(['Q' + str(1 + int(fn_state[1:])), 'λ', 'Q' + str(1 + int(st_state[1:]))])
    #return the closure NFA
    return ObjectNFA(status, alphabetstarget, transitions, start, final)



def create_nfa(postfix_regex):
    #build NFA from postfix regex
    nfa_stack = []

    for char in postfix_regex:
        if validate_alphabet(char):
            nfa_stack.append(regex_to_nfa(char))
        elif char == "*":
            nfa_stack.append(closure_nfa(nfa_stack.pop()))
        elif char == "+":
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa_stack.append(combine_nfa(nfa1, nfa2))
        elif char == ".":
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa_stack.append(nfa_concatenate(nfa1, nfa2))

    return nfa_stack.pop()
    

def infix_to_postfix(regex):
    #convert regex to postfix
    precedence = {
        '+': 1,
        '.': 2,
        '*': 3
    }
    postfix_regex = ""
    stack = []

    for char in regex:
        if  (char == '*') or validate_alphabet(char):
            postfix_regex += char
        elif char == ')':
            while ((len(stack) != 0) and (stack[-1] != '(')):
                postfix_regex += stack.pop()
            stack.pop()    
        elif char == '(':
            stack.append(char)
        else:
            while ((len(stack) != 0) and
                   (stack[-1] == '*' or stack[-1] == '.') and
                   (precedence[char] <= precedence[stack[-1]])
            ):
                postfix_regex += stack.pop()
            stack.append(char)

    while len(stack) != 0:
        postfix_regex += stack.pop()

    return postfix_regex





def convert_to_nfa(regular_expression):
    if regular_expression == "":
        return regex_to_nfa('λ')

    regular_expression = add_dot(regular_expression)
    regular_expression = infix_to_postfix(regular_expression)
    return create_nfa(regular_expression)


def read_re_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    expression = lines[1].replace('^', '')

    return expression


def write_file(path):
    # Writing status && Writing start state && Writing final states && Writing transition matrix
    with open(path, 'w', encoding='utf-8') as file:
        alphabetstarget = ' '.join(nfa.alphabetstarget)
        file.write(alphabetstarget + '\n')
        status = ' '.join(nfa.status)
        file.write(status + '\n')
        start_state = nfa.start[0]
        file.write(start_state + '\n')
        final = ' '.join(nfa.final)
        file.write(final + '\n')
        for arc in nfa.transitions:
            origin_state, input_letter, next_state = arc
            line = f"{origin_state} {input_letter} {next_state}\n"
            file.write(line)


if __name__ == '__main__':
    regex = read_re_from_file('RE_Input_3.txt')
    nfa = convert_to_nfa(regex)
    write_file('NFA_Output_3.txt')