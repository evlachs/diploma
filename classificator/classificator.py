from typing import Any
from scapy.all import rdpcap
from scapy.all import PacketList
import yaml
import datetime


class Classificator:
    def __init__(self, pcap_file_path: str, config_path: str):
        self.dump = rdpcap(pcap_file_path)
        self.config = self.__read_config_file(config_path)

    @staticmethod
    def __read_config_file(path: str) -> dict:
        with open(path) as file:
            config = yaml.safe_load(file)
        return config

    def get_protocol_sessions(self, protocol: str) -> dict[str, Any | PacketList]:
        packet_list = PacketList([packet for packet in self.dump if packet.haslayer(protocol)])
        protocol_sessions = packet_list.sessions()
        return protocol_sessions

    def get_session_parameters(self, session: dict[str, Any | PacketList]):
        avg_packet_size = 0
        avg_bitrate = 0
        for num, packet in enumerate(session.values(), 1):
            print(packet.len, datetime.datetime.fromtimestamp(float(packet.time)))
