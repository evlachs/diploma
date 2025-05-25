from typing import Any
from scapy.all import rdpcap, PacketList


class Dump:
    def __init__(self, pcap_file_path: str):
        self.dump = rdpcap(pcap_file_path)

    def get_protocol_sessions(self, l3_protocol: str) -> dict[str, Any | PacketList]:
        packet_list = PacketList([packet for packet in self.dump if packet.haslayer(l3_protocol)])
        protocol_sessions = packet_list.sessions()
        return protocol_sessions

    def get_all_sessions(self):
        return self.dump.sessions()

