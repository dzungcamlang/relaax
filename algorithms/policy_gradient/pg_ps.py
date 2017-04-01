from pg_model import SharedParameters

from relaax.server.parameter_server.parameter_server_base import ParameterServerBase
from relaax.server.common.session import Session


class PGParameterServer(ParameterServerBase):
    def __init__(self):
        self.session = Session(PSGraph())
        self.session.run([self.session.graph.initialize])


class PSGraph(SharedParameters):
    pass
