class DFA:
    def __init__(self, states_set, alphabets_set, transitions_dict, start_state, accept_states_set):
        #set of states
        self.states = states_set
        #set of alphabets
        self.alphabets = alphabets_set
        #set dictionary of transition functions
        self.transitions = transitions_dict
        #set start state
        self.start = start_state
        #set accept states
        self.accept_states = accept_states_set
        #set current state
        self.current_state = start_state


def lambda_compute(states_set, transactions_dict):
    # compute the lambda closure base on given state
    closure_changed = True
    closure_set = set(states_set)
    current_states_set = set(states_set)
    
    while closure_changed:
        new_states_set = set()
        for state in current_states_set:
            if (state, 'λ') in transactions_dict:
                new_states_set.update(transactions_dict[(state, 'λ')])
        new_states_set = new_states_set - closure_set
        closure_changed = bool(new_states_set)
        
        closure_set.update(new_states_set)
        current_states_set = new_states_set

    return frozenset(closure_set)


def read_input(file_path):
    # Reading file
    #Remove new line character from each line
    with open(file_path, 'r') as file:
        lines = file.readlines()
    #first line contains the alphabets
    alphabets = lines[0].split()
    #second line contains the states.
    nfa_states_set = set(lines[1].split())
    #third line contains the start state.
    nfa_start_state = lines[2].strip()
    #fourth line contains the accept states.
    nfa_accept_states_set = set(lines[3].split())

    transactions_dict = {}
    for line in lines[4:]:
        parts = line.split()
        state_from = parts[0]
        symbol = parts[1]
        state_to = parts[2]
        
        if (state_from, symbol) in transactions_dict:
            transactions_dict[(state_from, symbol)].add(state_to)
        else:
            transactions_dict[(state_from, symbol)] = {state_to}
         #if symbol is lambda,set it to None
        if symbol == 'λ':
            symbol = None
            
    for key in transactions_dict:
        transactions_dict[key] = frozenset(transactions_dict[key])

    return alphabets, nfa_states_set, nfa_start_state, nfa_accept_states_set, transactions_dict


def nfa_to_dfa(file_path):
    #  # read the NFA input && #iterate over the unmarked states && convert NFA to DFA
    alphabets, nfa_states_set, nfa_start_state, nfa_accept_states_set, nfa_transactions_dict = read_input(file_path)
    dfa_states_list = []
    dfa_transactions_dict = {}
    dfa_start_state = frozenset([nfa_start_state])
    dfa_accept_states_list = []
    unmarked_states_list = [dfa_start_state]

    while len(unmarked_states_list) > 0:
        current_state = unmarked_states_list.pop(0)
        dfa_states_list.append(current_state)

        for alphabet in alphabets:
            next_state_set = set()
            for nfa_state in current_state:
                if (nfa_state, alphabet) in nfa_transactions_dict:
                    next_state_set.update(nfa_transactions_dict[(nfa_state, alphabet)])

            next_state = lambda_compute(
                states_set=next_state_set,
                transactions_dict=nfa_transactions_dict
            )

            if len(next_state) > 0 and next_state not in dfa_states_list:
                unmarked_states_list.append(next_state)
                
            if next_state:
                dfa_transactions_dict[(current_state, alphabet)] = frozenset(next_state)

        if len(current_state.intersection(nfa_accept_states_set)) > 0:
            dfa_accept_states_list.append(current_state)
 #return DFA
    return DFA(states_set=dfa_states_list,
               alphabets_set=alphabets,
               transitions_dict=dfa_transactions_dict,
               start_state=dfa_start_state,
               accept_states_set=dfa_accept_states_list)





def write_output(file_path, dfa_object):
    #Write DFA to file
    
   
    
    
    with open(file_path, 'w') as f:
        #first line contains  alphabets.
        f.write(' '.join(dfa_object.alphabets) + '\n')
         #second line contains  status.
        f.write(' '.join(str(state) for state in dfa_object.states) + '\n')
        #third line contains  start status.
        f.write(str(dfa_object.start) + '\n')
        #fourth line contains accept status.
        f.write(' '.join(str(state) for state in dfa_object.accept_states) + '\n')
        
        for transition in dfa_object.transitions:
            f.write(
                str(transition[0]) + ' ' + str(transition[1]) + ' ' + str(dfa_object.transitions[transition]) + '\n')

    with open(file_path, 'r') as file:
        content = file.read()
        content = content.replace("frozenset", "").replace(")", " ").replace("(", "")
     # Write to file
    with open(file_path, 'w') as file:
        file.write(content)


def main():
    dfa_obj = nfa_to_dfa(file_path='NFA_Input_2.txt')
    write_output(file_path='DFA_Output_2.txt', dfa_object=dfa_obj)

if __name__ == '__main__':
    main()