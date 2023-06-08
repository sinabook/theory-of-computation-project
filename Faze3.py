class Dfa:
    
    def __init__(self, states, sigma, initial_state, final_states,
                 delta):
        self.states = states
        self.sigma = sigma
        self.initial_state = initial_state
        self.final_states = final_states
        self.delta = delta
    def __str__(self):
        return f"states= {self.states}\nsigma= {self.sigma}\ninitial state= {self.initial_state}\nfinal states= {self.final_states}\ndelta= {self.delta}"
    
    def Empty(self):
        #we can check all string shorter or equal to the number of states on the language and if non of them get accepted the language is empty
        all_str=self.Constructor(len(self.states))
        for _str in all_str:
            if (self.accepted(_str)):
                print('The Language is not Empty')
                return False
            print('The Language is Empty')
            return True
    def Constructor(self, length):
        #Constructing the array of all strings with the defalut value of members of sigma
        all_str = self.sigma.copy()
        #copy is for that all changes done to all strings variable does not change the alphabet of strings
        num_sigma=len(self.sigma)
        for i in range(2, length + 1):
            #the reason the range starts at 2 is that strings with length of 1 are just the alphabet themslves and the procedure is
            #we stick members of alphabet to the strings that are accepted to make new ones
            start = len(all_str) - (num_sigma**(i - 1))
            end = len(all_str)
            #we annexate the previous strings with alphabets
            for _str in all_str[start:end]:
                for letter in self.sigma:
                    all_str.append(_str + letter)
        return all_str
    def accepted(self, _str):
        #Is by defualt the start state
        current_state = self.initial_state
        for char in _str:
            #in this loop for every member of sigma we call the transition function
            next_state = self.delta[current_state][char]
            current_state = next_state
            #this means if the last letter ends us up in final state the string is accepted
        if (current_state in self.final_states):
            return True
        else:
            return False
    def Infinite(self):
        n = len(self.states)
        #this theorem was told in class
        str_lowerequal_2n_length = self.Constructor(2 * n)
        for _str in str_lowerequal_2n_length:
            if (len(_str) >= n and self.accepted(_str)):
                return True
        return False
    def lan_elements(self):
        if (self.Infinite()):
            print("The Language is Infinite")
        else:
            str_lowerequal_n_length = self.Constructor(len(self.states))
            elements = []
            for string in str_lowerequal_n_length:
                if (self.accepted(string)):
                    elements.append(string)
            return elements

    def num_elements(self):
        if (self.Infinite()):
            print("The langauge is Inifinte")
        else:
            return (len(self.lan_elements()))
    def Short(self):
        #we return the first element of the said array becuase we made strings by adding alphabets to previous ones
        
            n=len(self.states)
            if (self.Infinite()):
                str_lowerequal_2n_length = self.Constructor(2 * n)
                for _str in str_lowerequal_2n_length:
                    if (self.accepted(_str)):
                        return _str
            else:
                short = self.lan_elements()[0]
                return (short)
        

    def Long(self):
        
            if (self.Infinite()):
                print("The Language is infinite!")
            else:
                if len(self.lan_elements())!=0:
                    length = self.num_elements()
                    long = self.lan_elements()[length - 1]
                    return (long)
    def two_strings(self):
        accepted_str=[]
        not_accepted_str=[]
        str_lowerequal_n_length = self.Constructor(len(self.states))
        for string in str_lowerequal_n_length:
            if (self.accepted(string)):
                if(len(accepted_str)!=2):
                    accepted_str.append(string)
                else :   
                    if(len(not_accepted_str)!=2):
                        not_accepted_str.append(string) 
                        
        return [accepted_str,not_accepted_str]
        
    def all_str_len_k_num_m(self,k):
        
        counter=0
        accepted_str=[]
        str_lowerequal_n_length = self.Constructor(len(self.states))
        for string in str_lowerequal_n_length:
            if (self.accepted(string)):
                if(len(string)==k):
                    accepted_str.append(string)
                    counter+=1
                    
                
                    
        return [accepted_str,counter]
    def Complement(self):
        new_final = list(set(self.states) - set(self.final_states))
        comp = Dfa(self.states, self.sigma, self.initial_state,
                            new_final, self.delta)
        return comp

    def Operation(self, language):
        #Combination
        delta_f= {}
        initial = self.initial_state + language.initial_state
        Combination = [initial]#list of combined states with the defalut value of start states of each language
        S = 0 
        been_saw = []
        #the procedure is that we start from the first combined start states and work only on reachable states
        #and also there is a possibility that a combination goes to itself so we should consider not working on repeated ones
        while (S < len(Combination)):
            
            if (Combination[S] in been_saw):
                S += 1
                continue
            else:
                states = Combination[S] 
                been_saw.append(Combination[S])
                current_state_1 = states[0]
                current_state_2 = states[1]
                state_value = {}
                for symbols in self.sigma:
                    #for each of the alphabet we check that where does the annexated state go
                    next_state_1 = self.delta[current_state_1][symbols]
                    next_state_2 = language.delta[current_state_2][symbols]
                    next_state = next_state_1 + next_state_2
                    Combination.append(next_state)
                    state_value.update({symbols: next_state})#making a dictionary inside a transition function
                delta_f.update({states: state_value})
                S += 1
        Combination = list(set(Combination))#we turn this into a set so we get rid of repeated combinations
        #accepted states
        U_F_S = []#union final states
        I_F_S = []#intersection final states
        S_1_2_F_S = []#L1-l2 final states
        S_2_1_F_S = []#L2-L1 final states
        for states in Combination:
            current_state_1 = states[0]
            current_state_2 = states[1]
            #union
            if ((current_state_1 in self.final_states)
                    or (current_state_2 in language.final_states)):
                U_F_S.append(states)
            #intersection
            if ((current_state_1 in self.final_states)
                    and (current_state_2 in language.final_states)):
                I_F_S.append(states)
            #l1-l2
            if ((current_state_1 in self.final_states)
                    and not (current_state_2 in language.final_states)):
                S_1_2_F_S.append(states)
            #l2-l1
            if (not (current_state_1 in self.final_states)
                    and (current_state_2 in language.final_states)):
                S_2_1_F_S.append(states)
            #union P
            union = [Combination, language.sigma, initial, U_F_S,delta_f]
            
            #intersection
            intersection = [Combination, language.sigma, initial, I_F_S,delta_f]
            #print('\n\nThis is the DFA for Intersection of Languages \n %s' %(intersection))
            #l1-l2 P
            subtraction_l1l2 = [Combination, language.sigma, initial, S_1_2_F_S,delta_f]
            #print('\n\nThis is the DFA for L1-L2 \n %s' % (subtraction_l1l2))

            #l2-l1 P
            subtraction_l2l1 = [Combination, language.sigma, initial, S_2_1_F_S,delta_f]
            #print('\n\nThis is the DFA for L2-L1 \n %s' % (subtraction_l2l1))
        print('This is the DFA for Union of Languages \n %s' % (union))
        print('\n\nThis is the DFA for Intersection of Languages \n %s' %(intersection))
        print('\n\nThis is the DFA for L1-L2 \n %s' % (subtraction_l1l2))
        print('\n\nThis is the DFA for L2-L1 \n %s' % (subtraction_l2l1))
        #if both are each others subset they are equal
        if ((len(S_1_2_F_S) == 0)
                and (len(S_2_1_F_S) == 0)):
            print('L1 and L2 are Equals')
        #if neither is subset of each other they are seprated
        if ((len(S_1_2_F_S) != 0)
                and (len(S_2_1_F_S) != 0)):
            print('L1 and L2 are the Seperated')
    def minimizing(self):
        Possible_combs = []#list that contains all combinations of states
        for i in self.states:
            for j in self.states:
                if ((i != j) and not (j + i in Possible_combs)):
                    Possible_combs.append(i + j)
        marked_combs = []
        count = 1
        while (True):
            end = 0#if we dont mark any state on one attempt this ends the loop
            #mark states if only one of them is final and the other is not
            if (count == 1):
                for comb in Possible_combs:
                    current_state_1 = comb[0]
                    current_state_2 = comb[1]
                    if ((current_state_1 in self.final_states
                         and current_state_2 not in self.final_states)
                            or (current_state_1 not in self.final_states
                                and current_state_2 in self.final_states)):
                        marked_combs.append(comb)
                        end += 1
                count += 1

            else:
                for comb in Possible_combs:
                    if (comb not in marked_combs):#mark states that are not marked
                        current_state_1 = comb[0]
                        current_state_2 = comb[1]
                        for symbols in self.sigma:#check if marked state is reachable
                            next_state_1 = self.delta[current_state_1][symbols]
                            next_state_2 = self.delta[current_state_2][symbols]
                            next_state = next_state_1 + next_state_2
                            next_state_reverse = next_state_2 + next_state_1
                            if (next_state in marked_combs
                                    or next_state_reverse in marked_combs): 
                                marked_combs.append(comb)
                                end += 1
                                break
            if (end == 0):#if no states were marked jump out
                break
            count += 1
        unmarked_combs = list(set(Possible_combs) - set(marked_combs))
        if(len(unmarked_combs)!=0):#this allows us to know if the state is already minimized or not and if all pairs of states are marked this means the state is minimized
            minimized_states = []#we find all states that are put togehter and rename all of them into a singular state
            for i in self.states:
                for n in range(len(unmarked_combs)):
                    if (i in unmarked_combs[n]):
                        break
                    if (n == (len(unmarked_combs) - 1)):
                        minimized_states.append(i)
            print(unmarked_combs)
            unmarked_combs.sort()
            equal_states = {}
        
            print(unmarked_combs)
            for comb in unmarked_combs:
                if (equal_states != {}):
                    key = list(equal_states.keys())
                    print(key)
                    for n in range(len(key)):
                        print(equal_states[key[n]])
                        if (comb[0] in equal_states[key[n]]):
                            equal_states[key[n]].add(comb[1])
                            print(equal_states[key[n]])
                            break
                        if (n == (len(key) - 1)):
                            equal_states.update({comb[0]: {comb[0], comb[1]}})
                else:
                    equal_states.update({comb[0]: {comb[0], comb[1]}})
                    print(equal_states)
            print(equal_states)
            #in this loop we add all states that are the same into our set of minimized states
            for keys in equal_states.keys():
                minimized_states.append(list(equal_states[keys]))
            print(minimized_states)
            #making a new delta and finding a new final and start state
            new_final_states = []
        
            for states in minimized_states:
                if (self.initial_state in states):
                    new_initial = states
                for final in self.final_states:
                    if (final in states):
                        new_final_states.append(states)
                        break
            #delta
            new_delta = {}
            for state in minimized_states:
                new_value_dict = {}
                for symbols in self.sigma:
                    simple_value = self.delta[state[0]][symbols]
                    for destination in minimized_states:
                        if (simple_value in destination):
                            value_in_form = destination  
                    new_value_dict[symbols] = value_in_form
                new_delta.update({str(state): new_value_dict})
            print(new_delta)
            print(
                "\n************This Is The Minimized DFA for Your Selected Language************\nstates= %s\nsigma= %s\ninitial state= %s\nfinal states= %s\ntransition function= %s"
                % (minimized_states, self.sigma, new_initial, new_final_states,
                   new_delta))
        else:
            print('Your DFA is Minimized')
class Nfa:
    def __init__(self, states, sigma, initial_state, final_states,
                 delta):
        self.states = states
        self.sigma = sigma
        self.initial_state = initial_state
        self.final_states = final_states
        self.delta = delta
    def __str__(self):
        return f"states= {self.states}\nsigma= {self.sigma}\ninitial state= {self.initial_state}\nfinal states= {self.final_states}\ntransition function= {self.delta}"
    def Del_lambda(self):#this only prints the delta with out the lambda transition
        new_delta={}
        for state in self.states:
            all_delta={}
            for char in self.sigma:
                all_delta[char]=set()
            first_step = [state]
            Passed = []
            for element in first_step:#we add states that are reachable from our current state via one two.. lambda trans
                transition = list(self.delta[element].keys())
                if ('lambda' in transition and element not in Passed):#if state has lambda trans and we see it for the first time
                    Passed.append(element)
                    for trans in self.delta[element]['lambda']:
                        first_step.append(trans)

            for st in first_step:#in this loop we are going to specify  all alphabets's transitions for all reachable states
                
                transition=self.delta[st].keys()
                for symbol in self.sigma:
                    if(symbol in transition):#if the transition for the desierd alphabet existed add it to all-delta
                        all_delta[symbol].add(self.delta[st][symbol])
            keys=all_delta.keys()
            for sym in  keys:
                #in this loop we are going to add all lambda transitions after transitioning of alphabets to our all-delta
                #for example if we go from q0 to q1 via a and go from q1 to q2 and q3 via lambda we have that we can go from q0 to q2 and q3 via lambda
                value=list(all_delta[sym])
                #print(value)
                for item in value:
                    item_trans=self.delta[item]
                    if('$' in item_trans):
                        for trans in self.delta[item]['lambda']:
                            all_delta[sym].add(trans)
            for key in list(all_delta.keys()):
                if all_delta[key]==set() :
                    del all_delta[key]
            new_delta.update({state:all_delta})
        return new_delta
    def fa_converter(self):#transition to a non-standard fa(meaning that the names of states are a list) and then transitioning that into a standard fa
        
        build_delta=self.delta
        fa_states=[self.initial_state]#
        new_build_delta={}
        Passed=[]#becuase we are going through the fa list we might add a repeated state so we use passed 

        for state in fa_states:#deafult value equals to start state
            if(state not in Passed):
                value_dict={}
                Passed.append(state)
                for alpha in self.sigma:
                    value_dict[alpha]=set()

                for symbol in self.sigma:
                    #for each member of sigma we make an empty set and continuing if we have a transition
                    #the set updates accordingly
                    pak_state=[]#all states that we can go to from our current state with the alphabet(could be more than one)
                    #if the state that we choose on the fa was more than one we need to calculate all the alphabets transitions for all the states in the list
                    for single_state in state:
                        if(symbol in list(build_delta[single_state].keys())):
                            for  el in build_delta[single_state][symbol]:
                                pak_state.append(el)
                                value_dict[symbol].add(el)
                    
                    if(pak_state!=[] and pak_state not in fa_states):
                        fa_states.append(pak_state)
                new_build_delta.update({str(state):value_dict})#updating the delta of the converted fa
        print(new_build_delta)
        for st in list(new_build_delta.keys()):
            for sym in list(new_build_delta[st].keys()):
                if(new_build_delta[st][sym]==set()):
                    if('@' not in fa_states):
                        fa_states.append('@')
                        val={}
                        for char in self.sigma:
                            val[char]='@'
                        new_build_delta['@']=val
                    new_build_delta[st][sym]='@'
        #making a new final state
        new_final=[]
        for state in fa_states:
            for  final in self.final_states:
                if(final in state):
                    new_final.append(state)
                    break#if one of the previous final states are in the list it is enough to say that the new state is final
                        #building the elements the way that we can give to a automata first we rename all states from a-z this is because the standard name of a state is a single alphabet 
        
        print(fa_states)
        print(new_build_delta)
        state_mark=ord('A')
        fa_form_states=[]
        for states in fa_states:#this loop just renames states
            if(states!='@'):
                fa_form_states.append(chr(state_mark))
                state_mark+=1
        fa_form_states.append('@')
        str_form_states=[]
        for num in range(len(fa_states)-1):
            str_form_states.append(str(fa_states[num]))
            fa_states[num]=sorted(fa_states[num])
        #converting the delta into standard form
        build_delta_fa_form={}
        for key_state in new_build_delta.keys():
            if(key_state!='@'):
                index=str_form_states.index(key_state)
                key=fa_form_states[index]
            else:
                key='@'
            val={}
            for sym in new_build_delta[key_state].keys():
                if(new_build_delta[key_state][sym]!='@'):
                    value_index=fa_states.index(list(sorted(new_build_delta[key_state][sym])))
                    value_fa_form=fa_form_states[value_index]
                    val[sym]=value_fa_form
                else:
                    val[sym]='@'
            build_delta_fa_form[key]=val
        print(fa_states)
        print(fa_form_states)
        print(new_build_delta)
        print(build_delta_fa_form)
        final_fa_form=[]#doing the same for final and start states
        for state in new_final:
            index=fa_states.index(sorted(state))
            final_fa_form.append(fa_form_states[index])
        print(final_fa_form)
        initial_fa_form='A'

        return Dfa(fa_form_states,self.sigma,initial_fa_form,final_fa_form,build_delta_fa_form)
#inputs and functions for phase 3
L32= Dfa(
    ['A','B','C','D','E','F','G'], ['0', '1'], 'A',['E','B','C'], {
        'A': {
            '0': 'D',
            '1': 'B'
        },
        'B': {
            '0': 'C',
            '1': 'F'
        },
        'C': {
            '0': 'C',
            '1': 'F'
        },
        'D': {
            '0': 'A',
            '1': 'E'
        },
        'E': {
            '0': 'C',
            '1': 'F'
        },
        'F': {
            '0': 'F',
            '1': 'F'
        },
        'G': {
            '0': 'D',
            '1': 'E'
        },
        
    })
L31= Nfa(
    ['A','B','C','D','E'], ['a', 'b'], 'A',['E'], {
        'A': {
            'a':'A',
            'a':'B',
            'a':'C',
            'a':'D',
            'a':'E',
            'b': ['E','D']
        },
        'B': {
            'a': 'D',
            'b': 'E',
        },
        'C': {
            
            'b': 'C',
        },
        'D': {
            'a': 'E',
            'b': 'D',
        },
        'E': {},
        
        
    })
A=L31.fa_converter()
A.minimizing()
L32.minimizing()



            
