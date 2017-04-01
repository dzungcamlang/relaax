import concurrent
import grpc

import bridge_pb2

from bridge_message import BridgeMessage


class BridgeServer(object):
    def __init__(self, bind, session):
        self.server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=1))
        bridge_pb2.add_BridgeServicer_to_server(Servicer(session), self.server)
        self.server.add_insecure_port('%s:%d' % bind)

    def start(self):
        self.server.start()


class Servicer(bridge_pb2.BridgeServicer):
    def __init__(self, session):
        self.session = session

    def Run(self, request_iterator, context):
        ops, feed_dict = BridgeMessage.deserialize(request_iterator)
        result = self.session.run(
            self.map_ops(ops),
            self.map_feed_dict(feed_dict)
        )
        return BridgeMessage.serialize(result)

    def map_ops(self, ops):
        return [getattr(self.session.graph, op) for op in ops]

    def map_feed_dict(self, feed_dict):
        return {getattr(self.session.graph, k): v for k, v in feed_dict.iteritems()}
