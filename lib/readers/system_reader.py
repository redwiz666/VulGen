from lxml import etree, objectify
import lib.helpers.constants as constants
import os
import io
import re

from lib.objects.system import System
from lib.objects.module import Module

import sys

sys.dont_write_bytecode = True


class SystemReader:

    def read_scenario(scenario_file):
        systems = []
        print(f"Reading scenario file: {scenario_file}")
        doc = None
        xsd = None
        try:
            print(scenario_file)
            with open(scenario_file, "rb") as f:

                doc=etree.parse(io.BytesIO(f.read()))
                #xslt_doc=etree.parse(io.BytesIO(str.encode(f.read())))
                #transform=etree.XSLT(xslt_doc)
                #doc=transform(doc)
	            #doc = etree.XML(xslt_doc)
        except FileNotFoundError:
           print('Failed to read scenario configuration file')
           exit

        # validate scenario XML against schema
        #TODO: Add validation scheme
        #print(etree.tostring(doc, pretty_print=True))
        #r = doc.xpath('/scenario/system')
        #print(len(r))
        #remove namespace to make processing easier
        root = doc.getroot()
        
        ####   
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'): continue  # (1)
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i+1:]
            objectify.deannotate(root, cleanup_namespaces=True)
        ####

        #print(etree.tostring(doc, pretty_print=True))
        #r = doc.xpath('/scenario/system')
        #print(len(r))
        
        for system_node in doc.xpath('/scenario/system'):
            system_index = len(systems)
            module_selectors = []
            system_attributes = {}
            system_name = system_node.xpath('system_name/text()')
            #system_name = system_name
            print(f"system: " + system_name[0])

            # system attributes, such as basebox selection
            for attr in system_node.xpath('@*'):
                if attr.text != "" or attr.text != None:
                    if attr.name not in system_attributes.keys():
                        system_attributes[attr.name] = []
                    system_attributes[attr.name] = attr.text

            # literal values to store directly in a datastore
            for value in system_node.xpath('*[@into_datastore]/value'):
                name = value.text
                constants.datastore.append(name)

            # datastore in a datastore
            
            #if system_node.xpath('//*[@into_datastore]/datastore').to_s != ""
            #    Print.err "WARNING: a datastore cannot capture the values from another datastore (this will be ignored)"
            #Print.err "The scenario has datastore(s) that try to save directly into another datastore -- currently this is only possible via an encoder"
            #sleep 2

            # for each module selection
            for module_node in system_node.xpath('//vulnerability | //service | //utility | //build | //network | //base | //encoder | //generator'):
                # create a selector module, which is a regular module instance used as a placeholder for matching requirements
                module_selector = Module(module_node.tag)
                module_selector.system_number == (system_index + 1)

                # create a unique id for tracking variables between modules
                tree = etree.ElementTree(root)
                module_selector.unique_id = re.sub(r"/", '', tree.getpath(module_node))  
                # check if we need to be sending the module output to another module
                for inputs in module_node.xpath('parent::input'):
                    # Parent is input -- track that we need to send write value somewhere
                    # if we need to feed results to parent module
                    if inputs.xpath('@into'):
                        for input_parent in inputs.xpath('..'):
                            module_selector.write_output_variable = inputs.xpath('@into')
                            module_selector.write_to_module_with_id = re.sub('/[^a-zA-Z0-9]/', '',tree.getpath(input_parent))
                    # check if we need to send the module output to a datastore
                    if inputs.xpath('@into_datastore') != '':
                        module_selector.write_to_datastore = inputs.xpath('@into_datastore')
                    # check if we need to send the module path to a datastore (to ensure unique module selection)
                    if inputs.xpath('@unique_module_list') != '':
                        module_selector.write_module_path_to_datastore = inputs.xpath('@unique_module_list')

                # check if we are being passed an input *literal value*
                for input_value in module_node.xpath('input/value'):
                    variable = input_value.xpath('../@into/text()')
                    value = input_value.text
                    print(f"  -- literal value: {variable} = {value}")
                    if variable not in module_selector.received_inputs.keys():
                        module_selector.received_inputs[variable]=[]
                    module_selector.received_inputs[variable].append(value)

                # check if we are being passed a datastore as input
                for input_value in module_node.xpath('input/datastore'):
                    access = input_value.xpath('@access/text()')
                    if access == '':
                        access = 'all'

                    access_json = input_value.xpath('@access_json')
                    variable = input_value.xpath('../@into')
                    value = input_value.text
                    print(f"  -- datastore: {variable} = {value}")
                    tmp = []
                    tmp['variablename'] = value; tmp['access'] = access; tmp['access_json'] = access_json
                    module_selector.received_datastores[variable] = [].push(tmp)
            
                for attr in module_node.attrib.keys():
                    if attr != "" or attr != None:
                        if attr not in module_selector.attributes.keys():
                            module_selector.attributes[attr] = []
                        module_selector.attributes[attr].append(module_node.attrib[attr])

                print(f" {module_node.tag} ({module_selector.unique_id}), selecting based on:")
                for attr in module_selector.attributes.keys():
                    if attr and module_selector.attributes[attr] != "module_type":
                        print(f"  - {attr} ~= {module_selector.attributes[attr]}")


                # If this module is for this system
                if module_selector.system_number() == (system_index + 1):
                    # insert into module list
                    # if this module feeds output to another, ensure list order makes sense for processing...
                    if module_selector.write_output_variable != None:
                        print(f"  -- writes to: {module_selector.write_to_module_with_id} - {module_selector.write_output_variable}")
                        # insert into module list before the module we are writing to
                        insert_pos = -1 # end of list
                        for i in 0..len(module_selectors)-1:
                            if module_selector.write_to_module_with_id == module_selectors[i].unique_id:
                                # found position of earlier module this one feeds into, so put this one first
                                insert_pos = i

                        module_selectors.insert(insert_pos, module_selector)
                    else:
                        # otherwise just append module to end of list
                        module_selectors.append(module_selector)
        systems.append(System(system_name, system_attributes, module_selectors))

        return systems