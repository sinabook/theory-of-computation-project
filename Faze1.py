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
        #we check all string shorter or equal to the number of states on the language and if non of them get accepted the language is empty
        all_str=self.Constructor(len(self.states))
        for _str in all_str:
            if (self.accepted(_str)):
                print('The Language is not Empty')
                return False
            print('The Language is Empty')
            return True
    def Constructor(self, length):
        #constructing the array of all strings with the defalut value of members of sigma
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
L1= Dfa(
    ['A','B','C','E','F','G'], ['a', 'b'], 'A', ['A','B','C','F'], 
    {
        'A': {
            'a': 'B',
            'b': 'C'
        },
        'B': {
            'a': 'C',
            'b': 'C'
        },
        'C': {
            'a': 'E',
            'b': 'G'
        },
        'E': {
            'a': 'G',
            'b': 'F'
        },
        'F': {
            'a': 'G',
            'b': 'G'
        },
        'G': {
            'a': 'G',
            'b': 'G'
        },
        
    })
print("Accepted func")
print(L1.accepted('aba'))
print("Constructor func")
print(L1.Constructor(5))
print("Empty func")
L1.Empty()
print("Infinite func")
print(L1.Infinite())
print("lan_elements func")
print(L1.lan_elements())
print("num_elements func")
print(L1.num_elements())
print("Short func")
print(L1.Short())
print("Long func")
print(L1.Long())
print("two Strings func")
print(L1.two_strings())
print("Len m func")
print(L1.all_str_len_k_num_m(4))
print("Complement func")
print(L1.Complement())

            