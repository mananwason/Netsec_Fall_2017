from asyncio import *
import asyncio

from lab_1b.submission import RequestMovieInfo, RequestedInfoPacket, RequestAllDataPacket, AllDataPacket


class MoviesClient(Protocol):
    """
    This is our class for the Client's protocol. It provides an interface
    for sending a message. When it receives a response, it prints it out.
    """
    str = ""
    def __init__(self, callback=None):
        self.buffer = ""
        self.transport = None
        self.deserializer = RequestedInfoPacket.Deserializer()

    def connection_made(self, transport):
        print("Connected to {}".format(transport.get_extra_info("peername")))
        self.transport = transport

    def connection_lost(self, exc):
        self.transport = None
    def data_received(self, data):
        print(data)
        self.deserializer.update(data)

        for echoPacket in self.deserializer.nextPackets():
            if isinstance(echoPacket, RequestedInfoPacket):
                MoviesClient.str = echoPacket.parameter_info
            elif isinstance(echoPacket, AllDataPacket):
                MoviesClient.str = echoPacket.all_info_colon_separated

    def close(self):
        self.transport.close()
        self.transport = None

    def requestMovieInfo(self, movie_name, param_name):
        MoviesClient.str = ""
        echoPacket = RequestMovieInfo(movie_name=movie_name, parameter_name=param_name)
        self.transport.write(echoPacket.__serialize__())

    def requestAllInfo(self, movie_name):
        MoviesClient.str = ""
        echoPacket1 = RequestAllDataPacket(movie_name=movie_name, param="GEnre")
        self.transport.write(echoPacket1.__serialize__())
