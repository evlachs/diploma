import os
from typing import Any
from scapy.all import rdpcap, wrpcapng, PacketList

class Dump:
    def __init__(self, pcap_file_path: str):
        self.dump = rdpcap(pcap_file_path)

    def get_protocol_sessions(self, l3_protocol: str) -> dict[str, Any | PacketList]:
        packet_list = PacketList([packet for packet in self.dump if packet.haslayer(l3_protocol)])
        protocol_sessions = packet_list.sessions()
        return protocol_sessions

    def get_all_sessions(self) -> dict[str, Any | PacketList]:
        return self.dump.sessions()

    @staticmethod
    def save_session(session: PacketList, name: str, path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
        """NEED TO UPDATE"""
        wrpcapng(f'{path}/{name}', session)
