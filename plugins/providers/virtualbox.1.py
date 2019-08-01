import sys
import lib.helpers.constants

class virtualbox:

    def check_options(*args):
        for each in args:
            if each == '--esxi-user':
                print("ESXi Username : {0},",args)
                constants.options['esxiuser'] = args
            if each == '--esxi-pass':
                print("ESXi Password: *********")
                constants.options['esxipass'] = args
            if each == 'esxi-disktype':
                print("ESXi disk type: {0}", args)
                constants.options['esxidisktype'] = args


    commands = {
        "check_options": check_options
    }

    info = {
        "type" : "provider"
    }
