from os import read
import xml.etree.ElementTree as ET
from itertools import chain, combinations,product


# A data representation of NFA
# Object type is used in this case
class NFA:

    # initialize constructor for the NFA
    def __init__(self, file_name):

        # get ready for parsing XML data
        tree = ET.parse(file_name)
        self.root = tree.getroot()
        
        self.states = self.get_states()
        self.transitions = self.get_transitions()
        self.start = self.get_start_state()
        self.accepts = self.get_accepts()
        self.current_reached_states = [self.start]
        self.current_state = None

        print('states',self.states)
        print('start',self.start)
        print('accepts',self.accepts)
        print('get_transitions',self.transitions)
       
        
    # return a list of states 
    def get_states(self):
        states = []
        for sta in self.root.iter('state'):
            states.append(sta.attrib['name'])
        return states
    
     # return a start state
    def get_start_state(self):
        for state in self.root.iter("state"):
            if (state.find('initial') != None):
                return state.attrib['name']
    
    # return a list of accept states
    def get_accepts(self):
        accept_states = []
        for state in self.root.iter("state"):
            if(state.find('final') != None):
                accept = state.attrib['name']
                accept_states.append(accept)
                return accept_states

    # return value of 'name' attribute for state element by given id
    def get_state_name_by_id(self, state_id):
        for sta in self.root.iter('state'):
            if(sta.attrib['id'] == state_id):
                return sta.attrib['name']

    
    # return a dictionary of (State, Symbol) -> [State1, State2, State3 ...]
    # Key -> (State, Symbol)  Value -> [State1, State2, State3 ...]
    def get_transitions(self):
        transitions = {}

        for tran in self.root.iter('transition'):

            from_state_id = tran.find('from').text
            from_state_name = self.get_state_name_by_id(from_state_id)

            to_state_id = tran.find('to').text
            to_state_name = self.get_state_name_by_id(to_state_id)

            read_input = tran.find('read').text

            current_to_state_value = transitions.get((from_state_name, read_input))
            current_to_state_epsilon_value = transitions.get(from_state_name)

            # if read_input == None:
            #     transitions[from_state_name] = [to_state_name]
            # else: 
            #     epsilon_to_state_list = transitions[read_input]
            #     epsilon_to_state_list.append(to_state_name)
            #     transitions[read_input] = epsilon_to_state_list
            
            # check if the given key is existed in dict
            if (from_state_name, read_input) not in transitions:  
                transitions[(from_state_name, read_input)] = [to_state_name]
            
            else:
                # if read_input == None:
                #     epsilon_to_state_list = transitions.get(read_input)
                #     epsilon_to_state_list.append(to_state_name)
                #     transitions[read_input] = epsilon_to_state_list
                # else:

                # get the list of destination States, and apend a new State to it

                to_state_list = transitions.get((from_state_name, read_input))

                to_state_list.append(to_state_name)

                transitions[(from_state_name, read_input)] = to_state_list
                
        return transitions
    
    # generate all cartesion product of a ['0','1'](size up to 5)
    def get_all_cartesion_product(self):
        l = ['0', '1']
        result = []

        for i in range(6):
            generate_list = list(product(l, repeat=i))
            # convert a collection of a string to a string
            for e in generate_list:
                result.append(''.join(e))
        return result

    def epslion_move(self, l):
        if len(l) == 0:
            return
        else:
            if (l[0], None) in self.transitions: 
                self.current_reached_states.append(l[0])
                target_states = self.transitions[(l[0], None)]
                self.current_reached_states.extend(target_states)
                self.epslion_move(target_states)
            else:
                self.current_reached_states.append(l[0])
                self.epslion_move(l[1:])
        self.current_reached_states = set(self.current_reached_states)

    # find all current reached states
    def run_current_case(self, current_input, current_states):
        new_reached_states = []

        for reached in current_states:
            if ((reached, current_input) in self.transitions):
                target = self.transitions[(reached, current_input)]
                new_reached_states.extend(target)

            else:
                new_reached_states.append(reached)
                # return False

        # new_reached_states = list(set(new_reached_states))
        self.current_reached_states.extend(new_reached_states)
        self.epslion_move(new_reached_states)
        
        
      

    # run nfa and check if the program will accpet the given input
    # return true when NFA accepts the input, false otherwise
    def run_nfa(self, str_input):
        # each string
        input_list = list(str_input)
        # reset current state when a new input is given

        self.current_reached_states = [self.start]
        
        for inp in input_list:
            self.run_current_case(inp, self.current_reached_states)
        # check current state is in accept states or not
        # if (self.current_state in self.accepts):
        if any(state in self.accepts for state in self.current_reached_states):
            return True
        else:
            return False            

    
    #find the language that a DFA recognizes (all possible string inputs accepted by DFA)
    def find_all_accepted_inputs(self):
        all_inputs = self.get_all_cartesion_product()
        print(all_inputs)
        # filter out all inputs that rejected by DFA, keep rest of them that accepted by DFA
        accepted_inputs = filter(self.run_nfa, all_inputs)

        return accepted_inputs


def main():

    str_input = "fig1.27-nfa.jff"
    nfa = NFA(str_input)
    nfa.epslion_move(['q1','q2'])
    # print('move',s)
    # s = nfa.run_current_case('1', ['q1', 'q3'])
    # print('??', s)
    # nfa.run_nfa('11')
    # print(nfa.transitions)
    # accepts_inputs = list(nfa.find_all_accepted_inputs())
    # print('\n')
    # print(accepts_inputs)
    # print(nfa.current_reached_states)
    # s = nfa.run_nfa('1001')
    # print(s)
    # print('current_reached_states', nfa.current_reached_states)
    


if __name__ == "__main__":
    main()