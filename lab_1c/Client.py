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
        if callback:
            self.callback = callback
        else:
            self.callback = print
        self.transport = None
        self.deserializer = RequestedInfoPacket.Deserializer()

    def close(self):
        self.__sendMessageActual("__QUIT__")

    def connection_made(self, transport):
        print("Connected to {}".format(transport.get_extra_info("peername")))
        self.transport = transport

    def data_received(self, data):
        self.deserializer.update(data)

        for echoPacket in self.deserializer.nextPackets():
            if isinstance(echoPacket, RequestedInfoPacket):
                MoviesClient.str = echoPacket.parameter_info
            elif isinstance(echoPacket, AllDataPacket):
                MoviesClient.str = echoPacket.all_info_colon_separated

    def requestMovieInfo(self, movie_name, param_name):
        MoviesClient.str = ""
        echoPacket = RequestMovieInfo(movie_name=movie_name, parameter_name=param_name)
        self.transport.write(echoPacket.__serialize__())

    def requestAllInfo(self, movie_name):
        MoviesClient.str = ""
        echoPacket1 = RequestAllDataPacket(movie_name=movie_name, param="GEnre")
        self.transport.write(echoPacket1.__serialize__())
