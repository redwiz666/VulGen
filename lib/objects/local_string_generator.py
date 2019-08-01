import getopt
import base64
import sys

# Inherited by local string generators
# stdout used to return value
# use Print.local to print status messages (formatted to stdout)

# A nice side-effect is that each of these modules is also an executable script

class StringGenerator:

    outputs = []

    # override this
    def __init__(self):
        # default values
        self.module_name = 'Null generator'
        self.has_base64_inputs = False
        self.outputs = []

    # override this
    def generate():
        outputs = []
        StringGenerator.read_arguments()

    def read_arguments():
        # Get command line arguments
        print('Reading args from STDIN')
        if len(sys.argv) == 0:
            try:
                opts, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', get_options_array())
            except getopt.GetoptError as err:
                # Do nothing...
                pass

        # process option arguments
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
            elif opt in ('--b64'):
                StringGenerator.has_base64_inputs = True
                # Decode if required
                if StringGenerator.has_base64_inputs:
                    argument = base64.b64decode(arg)
                else:
                    argument = arg
            process_options(opt, argument)

    # Override this when using read_fact's in your module
    def get_options():
        return get_options_array()

    def get_options_array():
        ['help','b64',]
        #[['--help', '-h', GetoptLong::NO_ARGUMENT],
        #['--b64', GetoptLong::OPTIONAL_ARGUMENT]]

    # Override this when using read_fact's in your module. Always call super first
    def process_options(self, opt, arg):
        if not option_is_valid(opt):
            print(f"Argument not valid: #{arg}")
            usage()
            sys.exit

        #case opt
        #when '--help'
        #    usage
        #when '--b64'
        #    # do nothing

    def usage():
        print(f"""Usage:
        #{sys.argv[0]} [--options]

        OPTIONS:
        --strings_to_encode [string]
        """)

    def run(self):
        print(self.module_name)

        read_arguments()

        print("Generating...")
        generate()

        # print the first 1000 chars to screen
        output = self.outputs.to_s
        length = len(output)
        if length < 1000:
            print(f"Generated: #{output}...")
        else:
            print("Generated: #{output.to_s[0..1000]}...")
            print(f"(Displaying 1000/#{length} length output)")

        enforce_utf8(self.outputs)
        if self.has_base64_inputs:
            print_outputs()


    def enforce_utf8(values):
        values = str(values).encode('UTF-8')


    def print_outputs():
        print(base64_encode_outputs)


    def base64_encode_outputs(self):
        self.outputs = map(base64.b64encode,self.outputs)


    def option_is_valid(opt_to_check):
        arg_validity = False
        valid_arguments = get_options_array()
        for valid_arg_array in valid_arguments:
            for valid_arg in valid_arg_array.each_with_index:
                if valid_arg == opt_to_check:
                    arg_validity = True
        return arg_validity

if __name__ == "__main__":
    StringGenerator.generate()