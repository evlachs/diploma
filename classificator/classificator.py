from typing import Any
from datetime import datetime
from scapy.all import PacketList


class Classificator:
    def __init__(self, session: dict[str, Any | PacketList]):
        self.session = session

    def classify_session(self, config: dict, session_params: dict[str, int | str]) -> [bool, str]:
        result = "Session {} is classified: {}, {}"
        session_name = list(self.session)[0]
        session_proto = session_params['parent_protocol']
        session_bitrate = session_params['avg_bitrate']
        session_pkt_size = session_params['avg_pkt_size']
        for service in config['services']:
            service_name = list(service.keys())[0]
            for traffic_type in service[service_name]:
                name = list(traffic_type.keys())[0]
                parent_protocol = traffic_type[name][0]['parent_protocol']
                avg_bitrate = traffic_type[name][1]['avg_bitrate']
                avg_pkt_size = traffic_type[name][2]['avg_pkt_size']
                if parent_protocol != session_proto:
                    continue
                elif avg_bitrate[0] < session_bitrate < avg_bitrate[1] and avg_pkt_size[0] < session_pkt_size < avg_pkt_size[1]:
                    return [True, result.format(session_name, service_name, name)]
        return [False, f"Session {session_name} is not classified"]

    def get_session_params(self, session: dict[str, Any | PacketList]):
        size = 0
        packet_count = 0
        session_proto = list(session)[0].split()[0]
        session_packets = list(self.session.values())
        start_time = datetime.fromtimestamp(float(session_packets[0].time))
        end_time = datetime.fromtimestamp(float(session_packets[-1].time))
        session_time = (end_time - start_time).seconds
        for packet in session_packets:
            packet_count += 1
            size += packet.len
        pkt_size = size//packet_count
        bitrate = size*8//session_time if session_time > 0 else size*8
        params = {'parent_protocol': session_proto, 'avg_bitrate': bitrate, 'avg_pkt_size': pkt_size}
        return params
