import asyncio
import playground
import sys
from playground.network.common.Protocol import StackingProtocol, StackingProtocolFactory, StackingTransport

from lab_1e import Client
from lab_1e.Client import MoviesClient
from lab_1e.MovieServer import MoviesServer


class PassThrough1(StackingProtocol):
    def connection_made(self, transport):
        print("PT1 connection made")
        self.transport = transport
        self.higherProtocol().connection_made(self.transport)

    def connection_lost(self, exc):
        print("PT1 connection lost")
        self.transport = None
        self.higherProtocol().connection_lost(exc)


    def data_received(self, data):
        print("PT1 data recd")
        self.higherProtocol().data_received(data)


class PassThrough2(StackingProtocol):
    def connection_made(self, transport):
        print("PT2 connection made")
        self.transport = transport
        self.higherProtocol().connection_made(self.transport)


    def connection_lost(self, exc):
        print("PT2 connection lost")
        self.transport = None
        self.higherProtocol().connection_lost(exc)


    def data_received(self, data):
        print("PT2 data recd")
        self.higherProtocol().data_received(data)


def test():
    f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
    ptConnector = playground.Connector(protocolStack=f)

    playground.setConnector("PT1", ptConnector)
if __name__ == '__main__':
    test()
    mode = sys.argv[1]
    print (mode)
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)

    if mode.lower() == "server":
        coro = playground.getConnector("PT1").create_playground_server(lambda: MoviesServer(), 101)
        server = loop.run_until_complete(coro)
        print("Echo Server Started at {}".format(server.sockets[0].gethostname()))
        loop.run_forever()
        loop.close()

    elif mode.lower() == "client":
        coro = playground.getConnector("PT1").create_playground_connection(lambda: MoviesClient(), "20174.1.1.1",
                                                                      101)
        xPort, client = loop.run_until_complete(coro)
        client.requestMovieInfo("frozen", "genre")
        loop.run_forever()
        loop.close()



