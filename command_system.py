command_list = {}
adm_com_list = []

class Command:
   def __init__(self, states):
        self.description = ''
        for state in states:
            if state not in command_list.keys():
                command_list[state] = []
            command_list[state].append(self)

   def process(self, in_msg = ""):
       pass

class AdmCommand:
   def __init__(self):
        self.description = ''
        adm_com_list.append(self)

   def process(self, in_msg = ""):
       pass