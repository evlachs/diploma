from classificator import Classificator
from config_handler import Config
from dump_handler import Dump
import argparse
from datetime import datetime

DESCRIPTION = 'Software for classifying network traffic in a pcap file'
CONFIG_PATH = 'configs/services.yml'
SESSIONS_PATH = datetime.now().strftime('%d.%m.%y')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('input_file', help='path/to/input_file.pcap with packets for classification')
    parser.add_argument(
        '-c',
        '--config_file',
        action='store',
        default=CONFIG_PATH,
        help='path/to/config_file.yml with classification parameters'
    )
    parser.add_argument(
        '-o',
        '--classified_only',
        action='store_false',
        default=True,
        help='displays classification result for all sessions'
    )
    parser.add_argument(
        '-s',
        '--sessions_path',
        action='store',
        default=SESSIONS_PATH,
        help='path/to/directory for save classified sessions .pcap file'
    )
    parser.add_argument(
        '-d',
        '--save_disabled',
        action='store_true',
        default=False,
        help='disable sessions saving'
    )
    args = parser.parse_args()
    config = Config(args.config_file)
    dump = Dump(args.input_file)
    config_params = config.classification_params
    sessions = dump.get_all_sessions()
    for session_name, session_packets in sessions.items():
        classificator = Classificator(session_name, session_packets)
        session_params = classificator.get_session_params()
        result = classificator.classify_session(config_params, session_params)
        if args.classified_only:
            if result[0]: print(result[1])
        else:
            print(result[1])
        if result[0] and not args.save_disabled:
            print(args.save_disabled)
            dump.save_session(session_packets, result[2], args.sessions_path)
