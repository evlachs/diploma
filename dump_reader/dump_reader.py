from typing import Any
from scapy.all import rdpcap
from time import time


class DumpReader:
    def __init__(self, pcap_file: str):
        self.dump = rdpcap(pcap_file)
        self.sessions = self.dump.sessions()

    def session_processing(self):
        for dump in self.dump:
            print(dump.fields)
