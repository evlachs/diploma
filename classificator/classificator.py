from typing import Any
from scapy.all import rdpcap
from scapy.all import PacketList
import yaml
from datetime import datetime


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

    @staticmethod
    def get_session_params(session_proto: str, session: str | PacketList):
        size = 0
        packet_count = 0
        start_time = datetime.fromtimestamp(float(session[0].time))
        end_time = datetime.fromtimestamp(float(session[-1].time))
        session_time = (end_time - start_time).seconds

        for packet in session:
            packet_count += 1
            size += packet.len

        pkt_size = size//packet_count
        bitrate = size*8//session_time if session_time > 0 else size*8
        params = {'parent_protocol': session_proto, 'avg_bitrate': bitrate, 'avg_pkt_size': pkt_size}
        return params

    def check_session_affiliation(self, session_name: str, parameters: dict[str, int | str]):
        result = "Session {} is classified: {}, {}"
        session_proto = parameters['parent_protocol']
        session_bitrate = parameters['avg_bitrate']
        session_pkt_size = parameters['avg_pkt_size']

        for service in self.config['services']:
            service_name = list(service.keys())[0]
            for traffic_type in service[service_name]:
                name = list(traffic_type.keys())[0]
                parent_protocol = traffic_type[name][0]['parent_protocol']
                avg_bitrate = traffic_type[name][1]['avg_bitrate']
                avg_pkt_size = traffic_type[name][2]['avg_pkt_size']

                if parent_protocol != session_proto:
                    continue
                if avg_bitrate[0] < session_bitrate < avg_bitrate[1] and avg_pkt_size[0] < session_pkt_size < avg_pkt_size[1]:
                    return [True, result.format(session_name, service_name, name)]

        return [False, f"Session {session_name} is not classified"]






















        # def extract_config_params(config):
        #     if isinstance(config, list):
        #         for value in config:
        #             extract_config_params(value)
        #     elif isinstance(config, dict):
        #         for k, v in config.items():
        #             extract_config_params(v)
        #     else:
        #         result.append(config)
        # extract_config_params(self.config['services'])
        # return result
