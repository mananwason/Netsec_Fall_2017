from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, ListFieldType


class RequestMovieInfo(PacketType):
    DEFINITION_IDENTIFIER = "lab1b_mwason.MovieInfoPacket"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
        ("movie_name", STRING),
        ("parameter_name", STRING)
    ]

class RequestedInfoPacket(PacketType):
    DEFINITION_IDENTIFIER = "lab1b_mwason.RequestedInfoPacket"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
        ("parameter_info", STRING),
        ("parameter_name", STRING)
    ]

class RequestAllDataPacket(PacketType):
    DEFINITION_IDENTIFIER = "lab1b_mwason.RequestedAllDataPacket"
    DEFINITION_VERSION = "1.0"

class AllDataPacket(PacketType):
    DEFINITION_IDENTIFIER = "lab1b_mwason.AllDataPacket"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
        ("all_info_colon_separated", ListFieldType(STRING))
    ]

def basicUnitTest():

if __name__=="__main__":
    basicUnitTest()