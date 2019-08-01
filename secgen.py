#!/usr/bin/python
import time
import importlib
import os, sys, re
import glob
import subprocess
from shutil import rmtree
import getopt
from pathlib import Path

#used to share variables between modules
import lib.helpers.constants as constants

#required to read the scenarios
from lib.readers.module_reader import ModuleReader
from lib.readers.system_reader import SystemReader

from lib.objects.system import System

#used for plugins
from yapsy.PluginManager import PluginManager
import plugins.categories as categories

#used to not write pyc files
sys.dont_write_bytecode = True

MainModule = '__init__'

# Load the plugins from the plugin directory.
manager = PluginManager()
manager.setPluginPlaces(["plugins"])
#manager.setPluginInfoExtension("plugin")
manager.setCategoriesFilter({
   "Provider" : categories.IProvider
   })
manager.collectPlugins()

def usage():
    # Loop round the plugins and print their names.
    
    print(f"""Usage:
   {os.path.basename(__file__)} [--options] <command>
   OPTIONS:
   --scenario [xml file], -s [xml file]: Set the scenario to use
              (defaults to {constants.SCENARIO_XML})
   --project [output dir], -p [output dir]: Directory for the generated project
              (output will default to {default_project_dir()})
   --shutdown: Shutdown VMs after provisioning (vagrant halt)
   --network-ranges: Override network ranges within the scenario, use a comma-separated list
   --read-options [conf path]: Reads options stored in file as arguments (see example.conf)
   --memory-per-vm: Allocate generated VMs memory in MB (e.g. --memory-per-vm 1024)
   --total-memory: Allocate total VM memory for the scenario, split evenly across all VMs.
   --cpu-cores: Number of virtual CPUs for generated VMs
   --help, -h: Shows this usage information
   --system, -y [system_name]: Only build this system_name from the scenario
   --snapshot: Creates a snapshot of VMs once built
    """)

    for plugin in manager.getPluginsOfCategory('"Provider'):
        plugin.plugin_object.usage()
    
    print(f"""
    COMMANDS:
   run, r: Builds project and then builds the VMs
   build-project, p: Builds project (vagrant and puppet config), but does not build VMs
   build-vms, v: Builds VMs from a previously generated project
              (use in combination with --project [dir])
   ovirt-post-build: only performs the ovirt actions that normally follow a successful vm build
              (snapshots and networking)
   create-forensic-image: Builds forensic images from a previously generated project
              (can be used in combination with --project [dir])
   list-scenarios: Lists all scenarios that can be used with the --scenario option
   list-projects: Lists all projects that can be used with the --project option
   delete-all-projects: Deletes all current projects in the projects directory 

    """) 


# Builds the vagrant configuration file based on a scenario file
# @return build_number [Integer] Current project's build number
def build_config(scenario, out_dir, options):
    print('Reading configuration file for virtual machines you want to create...')
    # read the scenario file describing the systems, which contain vulnerabilities, services, etc
    # this returns an array/hashes structure
    #systems = SystemReader.SystemReader.read_scenario(scenario)
    

    #base_path = Path(__file__).parent; file_path = (base_path / scenario.replace(" ","")).resolve()

    systems = SystemReader.read_scenario(scenario)
    print(f"{len(systems)} system(s) specified")

    all_available_modules = ModuleReader.get_all_available_modules()

    print('Resolving systems: randomising scenario...')
    # update systems with module selections
    for system in systems:
        system.module_selections = System.resolve_module_selection(system, all_available_modules, options)
    
    print("Creating project: #{out_dir}...")
    # creates Vagrantfile and other outputs and starts the vagrant installation
    creator = projectFilesCreator(systems, out_dir, scenario, options)
    creator.write_files

    print('Project files created.')

# Builds the vm via the vagrant file in the project dir
# @param project_dir
def build_vms(scenario, project_dir, options):
    if not constants.PROJECT_DIR.contains(constants.ROOT_DIR):
        print('Relative path to project detected')
        project_dir = "#{ROOT_DIR}/#{project_dir}"
        print("Using #{project_dir}")

    project_dir + '/scenario.xml'

    print("Building project: #{project_dir}")
    system = ''
    command = 'up'
    if "system" in constants.options:
        system = options[:system]
    if "reload" in constants.options:
        command = '--provision reload'

    retry_count = 0
    successful_creation = False

    while retry_count and not successful_creation:
        try:
            vagrant_output =subprocess.check_output("vagrant " + project_dir + " " + command + " " + system)
        except subprocess.CalledProcessError:
            if subprocess.CalledProcessError.contains('exit 0'):
                print('VMs created.')
                successful_creation = True
            elif subprocess.CalledProcessError.contains('exit 1'):
                #TODO: Identify which VMs failed
                print('Error while creating VM')
        if "shutdown" in constants.options:
            print('Shutting down VMs.')
            time.sleep(30)
            subprocess.check_output('vagrant ' + project_dir + " " + 'halt')
    if successful_creation:
        if 'snapshot' in constants.options:
            print('Creating a snapshot of VM(s)')
            time.sleep(20) # give the provider a chance to save any VM config changes before creating the snapshot
            try:
                subprocess.check_output('vagrant ' + project_dir + " " + 'snapshot push')
            except subprocess.CalledProcessError:
                if subprocess.CalledProcessError.contains('exit 1'):
                    print('Error taking snapshot')
                elif subprocess.CalledProcessError.contains('exit 0'):
                    print("Snapshot taken successfully")
    else:
        print("Failed to build VMs")
        sys.exit(1)

def delete_virtualbox_vm(vm_name):
    print("Deleting VirtualBox VM {}".format(vm_name))
    #Print.info "VirtualBox VM #{vm_name} deleted" if system "VBoxManage unregistervm #{vm_name} --delete"

# Runs methods to run and configure a new vm from the configuration file
def run(scenario, project_dir, options):
    build_config(scenario, project_dir, options)
    build_vms(scenario, project_dir, options)

def default_project_dir():
    return str(constants.PROJECTS_DIR + "/SecGen" + time.strftime("%Y%m%d_%H%M%S"))

def project_dir(prefix):
    return str(constants.PROJECTS_DIR + "/" + prefix + "_SecGen" + time.new.strftime("%Y%m%d_%H%M%S"))

def list_scenarios():
    print("Full paths to scenario files are displayed below")
    for file in glob.iglob(constants.ROOT_DIR + "/scenarios/", recursive=True):
        if os.path.isfile(file) and file.endswith('.xml'):
            print(file)

def list_projects():
    print("Full paths to project directories are displayed below")
    for dir in glob.iglob(constants.PROJECTS_DIR + '/'):
        if os.isdir(dir):
            print(dir)

# Delete all current project directories
def delete_all_projects():
    rmtree(constants.PROJECTS_DIR + '/')

# returns an array containing the system names from the scenario
def get_vm_names(scenario):
    vm_names = []
    #TODO: Fix the parser referance below
    parser = "Nori.new"
    scenario_hash = parser.parse(File.read(scenario))
    #Print.debug "scenario_hash: #{scenario_hash}"
    if 'scenario' in scenario_hash: # work around for a parsing quirk
        scenario_hash = scenario_hash['scenario']
    if isinstance(scenario_hash['system'], list):
        for system in scenario_hash:
            vm_names << system['system_name']
    elif isinstance(system['system'], hash):
         vm_names << scenario_hash['system']['system_name']
    else:
        print("Not an array or hash")
        #print("Not an array or hash?: {}".format(scenario_hash['system']
    return vm_names

# end of method declarations
# start of program execuation

def main():   

    # Loop round the plugins and print their names.
    for plugin in manager.getAllPlugins():
        plugin.plugin_object.print_name()

    sys.argv.append('r')
    sys.argv.append('--esxi-user')
    sys.argv.append('root')
    #sys.argv.append('-s scenarios/default.xml')

    print('~' * 47)
    print('SecGen - Creates virtualised security scenarios')
    print('            Licensed GPLv3 2014-18')
    print('~'*47)


    # Get command line arguments
 
    scenario = constants.SCENARIO_XML
    project_dir = None

    # process option arguments
    options = ['help',
        'run',
        'project=',
        'scenario=',
        'prefix=',
        'system=',
        'reload',
        'memory-per-vm=',
        'total-memory=',
        'cpu-cores=',
        'shutdown',
        'network-ranges=',
        'snapshot',
        ]

    for plugin in manager.getPluginsOfCategory('Provider'):
        for each in plugin.plugin_object.get_options().keys():
            options.append(each)

    try:
        opts, remainder = getopt.gnu_getopt(sys.argv[1:], 'rs:',options)
    except getopt.GetoptError as err:
        print (str(err))
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-p', '--project'):
            project_dir = arg
        elif opt in ('--scenario', '-s'):
            scenario = arg.replace(" ", "")
        elif opt in ('--prefix'):
            constants.options['prefix'] = arg
            project_dir = project_dir(arg)

        # Additional options
        elif opt in ('--system'):
            print("VM control (Vagrant) commands will only apply to system {} (must match a system defined in the scenario)".format(arg))
            constants.options['system'] = arg
        elif opt in ('--relead'):
            print("Will reload and re-provision the VMs")
            constants.options['reload'] = True
        elif opt in '--snapshot':
            print("Taking snapshots when VMs are created")
            constants.options['snapshot'] = True

        for plugin in manager.getPluginsOfCategory('Provider'):
            if plugin.plugin_object.check_options(opt, arg):
                if constants.cur_provider == '':
                    print(f"Using {plugin.plugin_object.print_name()}")
                    constants.cur_provider = plugin
                    break;
                else:
                    print("You have specified arguments from 2 (or more) providers")
                    sys.exit(1)
                
        else:
            print("Argument not valid: {}".format(arg))
            usage()
            sys.exit(1)

    # at least one command
    if len(sys.argv) < 2:
        print('Missing command')
        usage()
        sys.exit(1)

    for cmd in remainder:
        if cmd in ('run', 'r'):
            if project_dir == None: project_dir = default_project_dir()
            run(scenario, project_dir, constants.options)
        elif cmd in ('build-project', 'p'):
            if project_dir == None: project_dir = default_project_dir()
            build_config(scenario, project_dir, constants.options)
        elif cmd in ('build-vms', 'v'):
            if project_dir:
                build_vms(scenario, project_dir, constants.options)
            else:
                print('Please specify project directory to read')
                usage()
                sys.exit(1)

        else:
            print(f'Command {remainder} unrecoginized')
            usage()
            sys.exit(1)

if __name__ == "__main__":
    main()