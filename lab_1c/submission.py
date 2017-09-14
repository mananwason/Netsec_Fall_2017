import asyncio
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToProtocol

from lab_1c.Client import MoviesClient
from lab_1c.MovieServer import MoviesServer


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


def overTheNetwork():
    loop = asyncio.get_event_loop()
    loop.create_server(lambda: MoviesServer(), port=8000)

    loop.create_connection(lambda: MoviesClient(), host='127.0.0.1', port=8000)

if __name__ == "__main__":
    basicUnitTest()
    # overTheNetwork()