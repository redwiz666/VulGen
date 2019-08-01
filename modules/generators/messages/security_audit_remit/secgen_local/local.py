#!/usr/bin/python

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
print(current_dir[:current_dir.rfind(path.sep + "modules")])
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep + "modules")])
from lib.objects.local_string_generator import StringGenerator
import lib.helpers.constants as constants
sys.path.pop(0)

from jinja2 import Template, BaseLoader

class SecurityAuditRemitGenerator(StringGenerator):
    business_name = ''
    business_location = ''
    local_backup = ''
    remote_backup = ''
    physical_security = ''

    LOCAL_DIR = current_dir[:current_dir.rfind(path.sep)]
    TEMPLATE_PATH = LOCAL_DIR + "/templates/security_audit_remit.md.erb"
    TEMPLATE_PATH = TEMPLATE_PATH.replace("/",'\\')

    def __init__(self):
        super
        self.module_name = 'Security Audit Remit Generator'
        self.business_name = ''
        self.business_location = ''
        self.local_backup = ''
        self.remote_backup = ''
        self.physical_security = ''

    def get_options_array():
        super
        ['name=', 
        'business_name='
        'business_location',
        'local_backup',
        'remote_backup',
        'physical_security']

    def process_options(opts):
        super
        for opt, arg in opts:
            if opt in ('--name'):
                self.name = arg
            elif opt in ('--business_name'):
                self.business_name = arg
            elif opt in ('--business_location'):
                self.business_location = arg
            elif opt in ('--local_backup'):
                self.local_backup = arg
            elif opt in ('--remote_backup'):
                self.remote_backup = arg
            elif opt in ('--physical_security'):
                self.physical_security = arg

    def generate():
        mydict = {"business_name":SecurityAuditRemitGenerator.business_name,
        "local_backup":SecurityAuditRemitGenerator.local_backup,"remote_backup":SecurityAuditRemitGenerator.remote_backup,"physical_security":SecurityAuditRemitGenerator.physical_security}
        dic = {}
        with open(SecurityAuditRemitGenerator.TEMPLATE_PATH) as file_:
            template = Template(file_.read())
        print(template.render(**mydict))


if __name__ == "__main__":
    SecurityAuditRemitGenerator.generate()