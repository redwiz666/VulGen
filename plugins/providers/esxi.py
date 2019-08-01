import sys
import lib.helpers.constants as constants
from plugins.categories import IProvider

sys.dont_write_bytecode = True

class IProviderPlugin(IProvider):
    
    def get_options(self):
        # this returns a dictorary with the options for the provider.
        # the format is switch : option
        return {'esxi-user=' : "esxiuser" , 'esxi-pass=' : "esxipass", 'esxi-disktype=' : "esxidisktype", 'esxi-url=' : 'esxiurl'}

    def check_options(self, opt, arg):
        found = False
        if opt in '--esxi-user':
            print("ESXi Username : {}".format(arg))
            constants.options['esxiuser'] = arg
            found = True
        elif opt in '--esxi-pass':
            print("ESXi Password : ********")
            constants.options['esxipass'] = arg
            found = True
        elif opt in '--esxi-url':
            print("ESXi host url : {}".format(arg))
            constants.options['esxiurl'] = arg
            found = True
        elif opt in '--esxi-datastore':
            print("ESXi datastore: {}".format(arg))
            constants.options['esxidatastore'] = arg
            found = True
        elif opt in '--esxi-network':
            print("ESXi Network Name : {}".format(arg))
            constants.options['esxinetwork'] = arg
            found = True
        elif opt in '--esxi-disktype':
            print("ESXi disk type : {}".format(arg))
            constants.options['esxidisktype'] = arg
            found = True
        return found

    def print_name(self):
        print('ESXi provider')

    def usage(self):
        print(f"""
        ESXI OPTIONS:
   --esxiuser [esxi_username]
   --esxipass [esxi_password]
   --esxi-url [esxi_api_url]
   --esxi-datastore [esxi_datastore]
   --esxi-disktype [esxi_disktype]
   --esxi-network [esxi_network_name]
        
        /n""")