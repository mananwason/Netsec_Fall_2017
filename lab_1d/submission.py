import asyncio

import playground
import sys
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToProtocol

from lab_1d.Client import MoviesClient
from lab_1d.MovieServer import MoviesServer


def basicUnitTest():
    asyncio.set_event_loop(TestLoopEx())
    server = MoviesServer()
    client = MoviesClient()
    transportToServer = MockTransportToProtocol(myProtocol=client)
    transportToClient = MockTransportToProtocol(myProtocol=server)
    transportToServer.setRemoteTransport(transportToClient)
    transportToClient.setRemoteTransport(transportToServer)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)
    client.requestMovieInfo("frozen", "genre")
    assert MoviesClient.str == "Comedy"
    assert MoviesServer.str == "genre"


if __name__ == "__main__":
    echoArgs = {}
    USAGE = """usage: echotest <mode>
      mode is either 'server' or a server's address (client mode)"""

    args = sys.argv[1:]
    i = 0
    for arg in args:
        if arg.startswith("-"):
            k, v = arg.split("=")
            echoArgs[k] = v
        else:
            echoArgs[i] = arg
            i += 1

    if not 0 in echoArgs:
        sys.exit(USAGE)

    mode = echoArgs[0]
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)

    if mode.lower() == "server":
        coro = playground.getConnector().create_playground_server(lambda: MoviesServer(), 101)
        server = loop.run_until_complete(coro)
        print("Echo Server Started at {}".format(server.sockets[0].gethostname()))
        loop.run_forever()
        loop.close()


    else:
        remoteAddress = mode
        coro = playground.getConnector().create_playground_connection(lambda: MoviesClient(), "20174.1.1.1", 101)
        transport, protocol = loop.run_until_complete(coro)
        print("Echo Client Connected. Starting UI t:{}. p:{}".format(transport, protocol))
        # loop.add_reader(sy    s.stdin, control.stdinAlert)
        # control.connect(protocol)
        loop.run_forever()
        loop.close()
