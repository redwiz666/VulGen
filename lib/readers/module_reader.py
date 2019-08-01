import sys
from lxml import etree, objectify
import lib.helpers.constants as constants
from lib.objects.module import Module
from lib.readers.system_reader import SystemReader
import glob
import io
import os
import re

sys.dont_write_bytecode = True

class ModuleReader:

  def get_all_available_modules():
    print(f'Reading available base modules...')
    all_available_bases = ModuleReader.read_bases()
    print(f"{len(all_available_bases)} base modules loaded")

    print(f'Reading available build modules...')
    all_available_builds = ModuleReader.read_builds()
    print(f"#{len(all_available_builds)} build modules loaded")

    print(f'Reading available vulnerability modules...')
    all_available_vulnerabilties = ModuleReader.read_vulnerabilities()
    print(f"#{len(all_available_vulnerabilties)} vulnerability modules loaded")

    print(f'Reading available service modules...')
    all_available_services = ModuleReader.read_services()
    print(f"#{len(all_available_services)} service modules loaded")

    print(f'Reading available utility modules...')
    all_available_utilities = ModuleReader.read_utilities()
    print(f"#{len(all_available_utilities)} utility modules loaded")

    print(f'Reading available generator modules...')
    all_available_generators = ModuleReader.read_generators()
    print(f"#{len(all_available_generators)} generator modules loaded")

    print(f'Reading available encoder modules...')
    all_available_encoders = ModuleReader.read_encoders()
    print(f"#{len(all_available_encoders)} encoder modules loaded")

    print(f'Reading available network modules...')
    all_available_networks = ModuleReader.read_networks()
    print(f"#{len(all_available_networks)} network modules loaded")

    # for each system, select modules
    return all_available_bases + all_available_builds + all_available_vulnerabilties + all_available_services + all_available_utilities + all_available_generators + all_available_encoders + all_available_networks

  # reads in all bases
  def read_bases():
    return ModuleReader.read_modules('base', constants.BASES_DIR, constants.BASE_SCHEMA_FILE, False)

  # reads in all build modules
  def read_builds():
    return ModuleReader.read_modules('build', constants.BUILDS_DIR, constants.BUILDS_SCHEMA_FILE, True)

  # reads in all vulnerability modules
  def read_vulnerabilities():
    return ModuleReader.read_modules('vulnerability', constants.VULNERABILITIES_DIR, constants.VULNERABILITY_SCHEMA_FILE, True)

  # reads in all services
  def read_services():
    return ModuleReader.read_modules('service', constants.SERVICES_DIR, constants.SERVICE_SCHEMA_FILE, True)

  # reads in all utilities
  def read_utilities():
    return ModuleReader.read_modules('utility', constants.UTILITIES_DIR, constants.UTILITY_SCHEMA_FILE, True)

  # reads in all utilities
  def read_generators():
    return ModuleReader.read_modules('generator', constants.GENERATORS_DIR, constants.GENERATOR_SCHEMA_FILE, True)

  # reads in all utilities
  def read_encoders():
    return ModuleReader.read_modules('encoder', constants.ENCODERS_DIR, constants.ENCODER_SCHEMA_FILE, True)

  # reads in all networks
  def read_networks():
    return ModuleReader.read_modules('network', constants.NETWORKS_DIR, constants.NETWORK_SCHEMA_FILE, False)

  # reads in xml files to create modules
  # @param [Object] module_type 'vulnerability', 'base', etc
  # @param [Object] modules_dir ROOT_DIR path leading to 'modules/'
  # @param [Object] schema_file the xml schema that defines this type of module
  # @param [Object] require_puppet whether this kind of SecGen module has puppet code
  # @return [Object] the list of modules read
  def read_modules(module_type, modules_dir, schema_file, require_puppet):
    modules = []
    path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), modules_dir)
    for dirpath, dirnames, files in os.walk(path):
        for name in files:
            if "secgen_metadata.xml" == name and os.path.isfile(os.path.join(dirpath, name)):
                module_path = dirpath
                module_filename = os.path.split(dirpath)[1]
                module_path = (os.path.relpath(os.path.join(dirpath))).replace("\\","/")

                print(f"Reading {module_type}: {module_path}")
                doc = None 
                xsd = None
                try:
                    with open(os.path.join(dirpath, name), "rb") as f:
                        doc=etree.parse(io.BytesIO(f.read()))
                except:
                    print(f"Failed to read {module_type} metadata file ({os.path.join(dirpath, name)})")
                    exit(1)

                # validate scenario XML against schema
                #TODO

                # remove xml namespaces for ease of processing
                root = doc.getroot() 
                for elem in root.getiterator():
                    if not hasattr(elem.tag, 'find'): continue  # (1)
                    i = elem.tag.find('}')
                    if i >= 0:
                        elem.tag = elem.tag[i+1:]
                    objectify.deannotate(root, cleanup_namespaces=True)

                new_module = Module(module_type)
                # save module path (and as an attribute for filtering)
                new_module.module_path = module_path
                new_module.attributes['module_path'] = [module_path]

                new_module.puppet_file = os.path.join(dirpath , module_filename + ".pp")
                new_module.puppet_other_path = os.path.join(dirpath , "manifests")

                # save executable path of any pre-calculation for outputs
                local = str(os.path.join(module_path,constants.MODULE_LOCAL_CALC_DIR))
                if os.path.isfile(local):
                    new_module.local_calc_file = local

                # check that the expected puppet files exist
                if require_puppet:
                    if not os.path.isfile(new_module.puppet_file):
                        print(f"Module {module_path} missing required puppet init file ({new_module.puppet_file})")
                        exit

                    if not os.path.isdir(new_module.puppet_other_path):
                        print(f"Module {module_path} missing required puppet module manifests folder ({new_module.puppet_other_path})")
                        exit

                # for each element in the vulnerability
                for module_doc in doc.xpath("/"+module_type+"/*"):

                # new_module.attributes[module_doc.name] = module_doc.content

                # creates the array if null
                    if module_doc.tag not in new_module.attributes.keys():
                        new_module.attributes[module_doc.tag] = []
                    new_module.attributes[module_doc.tag].append(module_doc.text)

                # for each conflict in the module
                for conflict_doc in doc.xpath("/"+module_type+"/conflict"):
                    conflict = {}
                    for node in conflict_doc:
                        if node.tag not in conflict_doc.keys():
                            conflict[node.tag] = []
                        conflict[node.tag].append(node.text)
                    new_module.conflicts.append(conflict)

                # for each dependency in the module
                for requires_doc in doc.xpath("/"+module_type+"/requires"):
                    require = {}
                    for node in requires_doc:
                        if node.tag not in require.keys():
                            require[node.tag] = []
                        require[node.tag].append(node.text)
                    new_module.requires.append(require)

                # for each default input
                for inputs_doc in doc.xpath("/"+module_type+"/default_input"):
                    for module_node in inputs_doc.xpath('descendant::vulnerability | descendant::service | descendant::utility | descendant::network | descendant::base | descendant::encoder | descendant::generator'):

                        # create a selector module, which is a regular module instance used as a placeholder for matching requirements
                        module_selector = Module(module_node.tag)
                        tree = etree.ElementTree(root)
                        # create a unique id for tracking variables between modules
                        module_selector.unique_id = (tree.getpath(module_node) + module_path).replace("/[^a-zA-Z0-9]", '')
                        # check if we need to be sending the module output to another module
                        for inputs in module_node.xpath('parent::input'):
                            # Parent is input -- track that we need to send write value somewhere
                            for input_parent in inputs.xpath('..'):
                                module_selector.write_output_variable = inputs.xpath('@into')
                                module_selector.write_to_module_with_id = (tree.getpath(input_parent)+module_path).replace("/[^a-zA-Z0-9]/", '')

                        if module_node.xpath('parent::default_input') != '':
                            # input for this module -- track that we need to send write value to the module itself
                            module_selector.write_output_variable = module_node.xpath('parent::default_input/@into')

                            module_selector.write_to_module_with_id = 'vulnerabilitydefaultinput'

                        # check if we are being passed an input *literal value*, into a module selector
                        for input_value in module_node.xpath('input/value'):
                            variable = input_value.xpath('../@into')
                            value = input_value.text
                            if variable[0] not in module_selector.received_inputs.keys():
                                module_selector.received_inputs[variable[0]] = []
                            module_selector.received_inputs[variable[0]].append(value)

                        into = module_node.xpath('ancestor::default_input/@into')

                        new_module.default_inputs_selectors[into[0]] = module_selector

                        for attr in module_node.attrib.keys():
                            if attr != "" or attr != None:
                                module_selector.attributes[attr] = [module_node.attrib[attr]]

                        """ for attr in module_node.xpath('@*'):
                            if attr != "" or attr != None:
                                module_selector.attributes[attr.tag] = attr """    
                        print(f" {module_node.tag} ({module_selector.unique_id}), selecting based on:")
          
                        for attr in module_selector.attributes:
                            if "module_type" not in [attr[0], attr[1]]:
                                print(f"  - {attr} ~= {module_selector.attributes[attr]}")

                    #check if we are being passed an input *literal value* -- to the containing module's default_value itself (as opposed to a module selector)
                    for input_value in inputs_doc.xpath('value'):
                        variable = input_value.xpath('parent::default_input/@into')
                        value = input_value.text
                        if variable[0] not in new_module.default_inputs_literals.keys():
                            new_module.default_inputs_literals[variable[0]] = []
                        new_module.default_inputs_literals[variable[0]].append(value)


                modules.append(new_module)

    return modules