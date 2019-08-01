import sys
import lib.helpers.constants as constants
from plugins.categories import IProvider

sys.dont_write_bytecode = True

class IProviderPlugin(IProvider):
    
    def get_options(self):
        # this returns a dictorary with the options for the provider.
        # the format is switch : option
        return {'gui-output' : False , 'nopae' : False, 'hwvirtex' : False, 'vtxvpid' : False, 'max-cpu-usage=' : "maxcpu", 'g' : False}

    def check_options(self, opt, arg):
        found = False
        if opt in ('--gui-output'):
            print("Gui output set (virtual machines will be spawned)")
            constants.options['gui_output'] = True
            found = True
        elif opt in '--nopae':
            print("no pae")
            constants.options['nopae'] = True
            found = True
        elif opt in '--hwvirtex':
            print("with HW virtualisation")
            constants.options['hwvirtex'] = True
            found = True
        elif opt in '--vtxvpid':
            print("with VT support")
            constants.options['vtxvpid'] = True
            found = True
        elif opt in '--memory-per-vm':
            if 'total_memory' in constants.options.keys():
                print('Total memory option specified before memory per vm option, defaulting to total memory value')
            else:
                print("Memory per vm set to {}".format(arg))
                constants.options['memory_per_vm'] = arg
            found = True
        elif opt in '--total-memory':
            if 'memory_per_vm' in constants.options.keys():
                print('Memory per vm option specified before total memory option, defaulting to memory per vm value')
            else:
                print("Total memory to be used set to {}".format(arg))
                constants.options['total_memory'] = arg
            found = True
        elif opt in '--cpu-cores':
            print("Number of cpus to be used set to {}".format(arg))
            constants.options['cpu_cores'] = arg
            found = True
        elif opt in '--max-cpu-usage':
            print("Max CPU usage set to {}".format(arg))
            constants.options['max_cpu_usage'] = arg
            found = True
        elif opt in '--shutdown':
            print('Shutdown VMs after provisioning')
            constants.options['shutdown'] = True
            found = True
        elif opt in '--network-ranges':
            print('Overriding Network Ranges')
            constants.options['ip_ranges'] = arg.split(',')
            found = True

        return found

    def print_name(self):
        print('Virtualbox provider')

    def usage(self):
        print(f"""
        VIRTUALBOX OPTIONS:
   --gui-output, -g: Show the running VM (not headless)
   --nopae: Disable PAE support
   --hwvirtex: Enable HW virtex support
   --vtxvpid: Enable VTX support
   --max-cpu-usage [1-100]: Controls how much cpu time a virtual CPU can use
                            (e.g. 50 implies a single virtual CPU can use up to 50% of a single host CPU)
        
        /n""")