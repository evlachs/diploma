from datetime import datetime
from scapy.all import PacketList


class Classificator:
    def __init__(self, session_name: str, session_packets: PacketList):
        self.session_name = session_name
        self.session_packets = session_packets

    def classify_session(self, services_params: dict[str, dict], session_params: dict[str, int | str]) -> list:
        result = "Session {} is classified: {}"
        session_proto = session_params['parent_protocol']
        session_bitrate = session_params['avg_bitrate']
        session_pkt_size = session_params['avg_pkt_size']
        for service in services_params:
            proto = service.split('.')[0]
            if proto != session_proto:
                continue
            bitrate = services_params[service]['avg_bitrate']
            pkt_size = services_params[service]['avg_pkt_size']
            if bitrate[0] <= session_bitrate <= bitrate[1] and pkt_size[0] <= session_pkt_size <= pkt_size[1]:
                return [True, result.format(self.session_name, service), service]
        return [False, f"Session {self.session_name} is not classified"]

    def get_session_params(self):
        size = 0
        packet_count = 0
        session_proto = self.session_name.split()[0]
        start_time = datetime.fromtimestamp(float(self.session_packets[0].time))
        end_time = datetime.fromtimestamp(float(self.session_packets[-1].time))
        session_time = (end_time - start_time).seconds
        for packet in self.session_packets:
            packet_count += 1
            try:
                size += packet.len
            except AttributeError:
                continue
        pkt_size = size//packet_count
        bitrate = size*8//session_time if session_time > 0 else size*8
        params = {'parent_protocol': session_proto, 'avg_bitrate': bitrate, 'avg_pkt_size': pkt_size}
        return params
