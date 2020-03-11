
import gremlinapi
from gremlinapi.exceptions import GremlinAuthError


class GremlinCLI(object):
    def __init__(self):
        super.__init__(self)

    def __call__(self):
        pass

    def do_action(self):
        pass

    def extend_parser(parser):
        subparsers = parser.add_subparsers(
            title="object", dest="what", help="Object to manipulate."
        )
        subparsers.required = True
        classes = []
