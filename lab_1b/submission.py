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
    FIELDS = [
        ("movie_name", STRING),
        ("param", STRING)
    ]
class AllDataPacket(PacketType):
    DEFINITION_IDENTIFIER = "lab1b_mwason.AllDataPacket"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
        ("all_info_colon_separated", ListFieldType(STRING))
    ]

def basicUnitTest():
    packet1 = RequestMovieInfo()
    packet1.movie_name = "Frozen"
    packet1.parameter_name = "Genre"
    packet1_ser = packet1.__serialize__()
    packet1_des = RequestMovieInfo.Deserialize(packet1_ser)
    assert packet1 == packet1_des

    packet2 = RequestedInfoPacket()
    packet2.parameter_name = "Genre"
    packet2.parameter_info = "Adventure"
    packet2_ser = packet2.__serialize__()
    packet2_des = RequestedInfoPacket.Deserialize(packet2_ser)

    assert packet2_des == packet2

    packet3 = RequestAllDataPacket()
    packet3.movie_name = "Frozen"
    data = ["ABC:123", "AVD:wer", "SDDS:4523"]
    packet3.all_info_colon_separated = data
    packet3_ser = packet3.__serialize__()
    packet3_des = RequestAllDataPacket.Deserialize(packet3_ser)

    assert packet3 == packet3_des


if __name__=="__main__":
    basicUnitTest()