class IProvider(object):
    """Plugins of this class are used as providers for the engine"""

    name = "No Format"

    def get_options():
        pass

    def print_name():
        print(name)

    def usage():
        pass