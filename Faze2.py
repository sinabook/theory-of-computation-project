class Dfa:
    
    def __init__(self, states, sigma, initial_state, final_states,delta):
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
                print("Language is infinite!")
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
            #union Print
            union = [Combination, language.sigma, initial, U_F_S,delta_f]
            
            #intersection Print
            intersection = [Combination, language.sigma, initial, I_F_S,delta_f]
            #print('\n\nThis is the DFA for Intersection of Languages \n %s' %(intersection))
            #l1-l2 Print
            subtraction_l1l2 = [Combination, language.sigma, initial, S_1_2_F_S,delta_f]
            #print('\n\nThis is the DFA for L1-L2 \n %s' % (subtraction_l1l2))

            #l2-l1 Print
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
#Inputs and functions for phase 2
L21 = Dfa(['A','B','C',], ['a', 'b'], 'A', ['A', 'B'], {
        'A': {
            'a': 'B',
            'b': 'A'
        },
        'B': {
            'a': 'C',
            'b': 'A'
        },
        'C': {
            'a': 'C',
            'b': 'C'
        }
    })
L22 = Dfa(
    ['P','Q','R',], ['a', 'b'], 'P', ['R'], {
        'P': {
            'a': 'Q',
            'b': 'P'
        },
        'Q': {
            'a': 'Q',
            'b': 'R'
        },
        'R': {
            'a': 'Q',
            'b': 'P'
        }
    })
Dfa.Operation(L21, L22)


