import xml.etree.ElementTree as ET
from itertools import chain, combinations,product


# A data representation of DFA
# Object type is used in this case
class DFA:

    # represent current state 
    current_state = None

    filename = input()

    tree = ET.parse(filename)
    root = tree.getroot()

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
        
    # return a list of states 
    def get_states(self):
        states = []
        for sta in self.root.iter('state'):
            states.append(sta.attrib['name'])
        return states

    # return a dictionary key-value pairs
    # Key -> (state, input)  Value -> state
    # (state, input) -> state
    def get_transitions(self):
        transitions = {}
        for tran in self.root.iter('transition'):

            from_state_id = tran.find('from').text
            from_state_name = self.get_state_name_by_id(from_state_id)

            to_state_id = tran.find('to').text
            to_state_name = self.get_state_name_by_id(to_state_id)

            read_input = tran.find('read').text
            
            transitions[(from_state_name, read_input)] = to_state_name

        return transitions
        
    # initialize constructor for the DFA
    def __init__(self):
        self.states = self.get_states()
        self.transitions = self.get_transitions()
        self.start = self.get_start_state()
        self.accepts = self.get_accepts()
        self.current_state = self.start

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

    # run DFA and check if the program will accpet the given input
    # return true DFA accepts the input, false otherwise
    def run_dfa(self, str_input):
        input_list = list(str_input)
        # reset current state when a new input is given
        self.current_state = self.start
        for inp in input_list:
            if ((self.current_state, inp) in self.transitions):
                self.current_state = self.transitions[(self.current_state, inp)]
            else:
                return False

        # check current state is in accept states or not
        if (self.current_state in self.accepts):
            return True
        else:
            return False


    
    #find the language that a DFA recognizes (all possible string inputs accepted by DFA)
    def find_all_accepted_inputs(self):
        all_inputs = self.get_all_cartesion_product()

        # filter out all inputs that rejected by DFA, keep rest of them that accepted by DFA
        accepted_inputs = filter(self.run_dfa, all_inputs)

        return accepted_inputs




def main():
    dfa = DFA()

    accepts_inputs = dfa.find_all_accepted_inputs()

    for inp in accepts_inputs: 
        print(inp)


if __name__ == "__main__":
    main()