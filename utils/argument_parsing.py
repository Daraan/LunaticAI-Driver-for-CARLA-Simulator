import argparse
from functools import wraps

# todo later: add some more flexible way to construct a parser. i.e. combine certain subparsers, e.g. one for port& host another one for settings

def subparser(func):
    """This decorator allows to join multiple subparsers in a flexible way."""
    @wraps(func)
    def wrapper(parser=None, *args, **kwargs):
        if parser is None: # create a parser if none is given
            parser = argparse.ArgumentParser()
        # else: TODO: are subparsers useful?
        func(parser, *args, **kwargs)
        return parser # return the parser object again
    
    # allows to circumvent calling the function. 
    # i.e. parser_function.parse_args() instead of parser_function().parse_args()
    wrapper.parse_args = lambda : wrapper(parser=None).parse_args() 
    # allows to adjust parsers by adding another parser or by adding a parser function
    wrapper.add = lambda parser: wrapper(parser) if isinstance(parser, argparse.ArgumentParser) else wrapper(parser())
    return wrapper


@subparser
def client_settings(parser):
    parser.add_argument('-p', '--port', help='TCP Port', default="2000", type=int)
    parser.add_argument('-i', '--host', help='Host', default="localhost", type=str)

@subparser
def interactive_mode(parser):
    parser.add_argument('-I', '--interactive', action='store_true', help='Interactive mode', default=False)


@subparser
def automatic_control_example(argparser):
    argparser.description = 'CARLA Automatic Control Client'
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='Print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1280x720',
        help='Window resolution (default: 1280x720)')
    argparser.add_argument(
        '--sync',
        action='store_true',
        help='Synchronous mode execution')
    argparser.add_argument(
        '--filter',
        metavar='PATTERN',
        default='vehicle.*',
        help='Actor filter (default: "vehicle.*")')
    argparser.add_argument(
        '--generation',
        metavar='G',
        default='2',
        help='restrict to certain actor generation (values: "1","2","All" - default: "2")')
    argparser.add_argument(
        '-l', '--loop',
        action='store_true',
        dest='loop',
        help='Sets a new random destination upon reaching the previous one (default: False)')

    # TODO: separate into subparsers
    argparser.add_argument(
        "-a", "--agent", type=str,
        choices=["Behavior", "Basic", "Constant"],
        help="select which agent to run",
        default="Behavior")
    argparser.add_argument(
        '-b', '--behavior', type=str,
        #choices=["cautious", "normal", "aggressive"],
        help='Choose one of the possible agent behaviors (default: normal) ',
        default='normal')

    argparser.add_argument(
        '-s', '--seed',
        help='Set seed for repeating executions (default: None)',
        default=None,
        type=int)
    argparser.add_argument(
        '-I', '--interactive',
        help='Enter interactive mode after initialization',
        action="store_true")