import json
from mock import Mock

from fixtures.mock_cmdl import cmdl
from fixtures.mock_utils import MockUtils
from relaax.server.rlx_server.rlx_config import options
from relaax.common.rlx_netstring import NetStringClosed
from relaax.server.rlx_server.\
    rlx_protocol.rawsocket.rlx_protocol import RLXProtocol, adoptConnection


class TestRlxProtocol:

    @classmethod
    def setup_class(cls):
        options.algorithm_module = Mock()
        cls.protocol = RLXProtocol('socket', ('localhost', 7000))

    @classmethod
    def teardown_class(cls):
        cmdl.restore()

    def test_adopt_connection_call_protocol_loop(self, monkeypatch):
        called_once = MockUtils.called_once(RLXProtocol, 'protocol_loop', monkeypatch)
        adoptConnection('socket', ('localhost', 7000))
        assert called_once[0] == 1

    def test_protocol_loop_general_exception(self, monkeypatch):
        monkeypatch.setattr(RLXProtocol, 'read_string', lambda x: '')
        monkeypatch.setattr(RLXProtocol, 'string_received',
                            lambda x, y: MockUtils.raise_(Exception('stop')))
        called_with = MockUtils.called_with(RLXProtocol, 'connection_lost', monkeypatch)
        try:
            self.protocol.protocol_loop()
            assert False
        except:
            assert called_with[0] == 'Unknown error'

    def test_protocol_loop_netstring_exception(self, monkeypatch):
        monkeypatch.setattr(RLXProtocol, 'read_string',
                            lambda x: MockUtils.raise_(NetStringClosed('stop')))
        called_with = MockUtils.called_with(RLXProtocol, 'connection_lost', monkeypatch)
        try:
            self.protocol.protocol_loop()
            assert False
        except:
            assert called_with[0] == 'Connection dropped'

    def test_connection_lost_do_nothing_wrong(self):
        try:
            self.protocol.connection_lost('reason')
            assert True
        except:
            assert False

    def test_string_received_and_send_string(self, monkeypatch):
        data = json.dumps({'response': 'ready'})
        protocol = RLXProtocol('socket', ('localhost', 7000))
        protocol.agent = Mock()
        protocol.agent.dataReceived = lambda x: x
        called_with = MockUtils.called_with(RLXProtocol, 'write_string', monkeypatch)
        protocol.string_received(data)
        assert called_with[0] == data
