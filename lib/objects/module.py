import lib.helpers.constants as constances
import re
import copy

#require 'digest/md5'
#require 'securerandom'

class Module:

    def __init__(self, module_type):
        self.module_type = module_type
        self.conflicts = []
        self.requires = []
        self.attributes = {}
        self.output = []
        self.write_output_variable = None
        self.write_to_module_with_id = ""
        self.received_inputs = {}
        self.received_datastores = {} # into_variable => [[variablename] and [access], ]
        self.default_inputs_selectors = {}
        self.default_inputs_literals = {}
        self.module_path = ""
        self.write_to_datastore = ""
        self.write_module_path_to_datastore = ""
        self.unique_id = ""
        self.puppet_file = ""
        self.puppet_other_path = ""
        self.local_calc_file = ""

    def inspect(self):
        return "SECGEN_MODULE(type:"+self.module_type+" path:" +self.module_path+" attr:"+self.attributes.inspect()+" to:"+self.write_to_module_with_id+"."+self.write_output_variable+" id:"+self.unique_id+" received_inputs:"+self.received_inputs+" default_inputs_selectors: "+self.default_inputs_selectors+" default_inputs_literals: "+self.default_inputs_literals

 
     # @return [Object] a string for console output
    def to_s(self):
        return """
    {self.module_type}: {self.module_path}\n
      attributes: {self.attributes.inspect}\n
      conflicts: {self.conflicts.inspect}\n
      requires: {self.requires.inspect}\n
      puppet file: {self.puppet_file}\n
      puppet path: {self.puppet_other_path}\n
        """

  # @return [Object] a string for Vagrant/python file comments
    def to_s_comment(self):
        out = input = ''
        if self.received_inputs != {}:
            input = "\n    #   received_inputs: "+self.received_inputs
        if self.write_to_module_with_id != '':
            out = "\n    #   writes out ('"+self.output+"') to "+self.write_to_module_with_id

        string = """
    # {self.module_type}: {self.module_path}
    #   id: {self.unique_id}
    #   attributes: {self.attributes.inspect}
    #   conflicts: #{self.conflicts.inspect}
    #   requires: {self.requires.inspect}{self.input}{self.out}
    """

  # @return [Object] the leaf directory (last part of the module path)
    def module_path_end(self):
        match = self.module_path.match("/.*?([^\/]*)$/i")
        return match.captures[0]

  # @return [Object] the module path with _ rather than / for use as a variable name
    def module_path_name(self):
        module_path_name = copy(module_path_name)
        module_path_name = module_path_name.replace('/','_')

  # @return [Object] a list of attributes that can be used to re-select the same modules
    def attributes_for_scenario_output(self):
        attr_flattened = {}

        for key, array in attributes:
            if key not in ['module_type', 'conflict', 'default_input', 'requires']:
                # creates a valid regexp that can match the original module
                attr_flattened[key] = re.escape(array.join('~~~')).replace("/\n\w*/, '.*'").replace("/\\ /, ' '").replace("/~~~/, '|'")
        return attr_flattened

  # A one directional test for conflicts
  # Returns whether this module specifies it conflicts with the other_module.
  # Each conflict can have multiple conditions which must all be met for this
  # to be considered a conflict. However, only one conflict needs to be satisfied.
  # @param [Object] other_module to compare with
  # @return [Object] boolean
    def conflicts_with(self, other_module):
        # for each conflict
        for conflict in self.conflicts:
            if other_module.matches_attributes_requirement(conflict):
                return True
            else:
                return False

    def matches_attributes_requirement(self, required):
        for require_key in required.keys():
          key_matched = False
          # Check to see if the required key is listed
          if require_key in self.attributes.keys():
            # Iterating over the required values
            for required_value in required[require_key]:
              #Iterate over the module values 
              for value in self.attributes[require_key]:
                #Check if the required value is in the module value
                if re.match(str(required_value).replace("'", '"'),value):
                  key_matched = True
                  break

        # any failure to match
        if not key_matched:
            return False

        return True

    def prepare_required_value(self, required_key, value):
      if required_key == 'module_path':
        # allow omission of 'modules/' e.g. <module_path>services/platform/module_name</module_path>
        if value.partition('/')[0] != 'modules':
          value = 'modules/' + value
        # wrap value with ^ and $ to limit start/end of string.
        value = "^{value}$"
      elif required_key == 'privilege' or required_key == 'type':
        value = "^{value}$"
      return value

  # Get the system that this module is for, based on the unique_id.
  # If there is more that 1 system we gets the first integer e.g. the 1 in scenariosystem1
    def system_number(self):
      split_string_array = self.unique_id.split('scenariosystem')
      tmp = split_string_array[1][0]
      if tmp.isdigit() == False:
        return 1 # only 1 system so return 1
      elif tmp.isdigit():
        return int(split_string_array[1][0]) # return the system id

    def printable_name(self):
        #return "{self.attributes['name'][0]} ({self.module_path})"

        return {self.attributes['name'][0]}


