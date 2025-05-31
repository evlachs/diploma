import logging
import argparse
from datetime import datetime
from dump_handler import Dump
from config_handler import Config
from classificator import Classificator


FORMAT = '%(asctime)s : %(filename)s : %(levelname)s : %(message)s'
LEVEL = logging.INFO

DESCRIPTION = 'Software for classifying network traffic in a pcap file'
CONFIG_PATH = 'configs/services.yml'
SESSIONS_PATH = f'saved_sessions/{datetime.now().strftime('%d.%m.%y')}'

if __name__ == '__main__':
    logging.basicConfig(filename='logs/traffic_classifier.log', format=FORMAT)
    logger = logging.getLogger(__name__)
    logger.setLevel(LEVEL)
    console = logging.StreamHandler()
    console.setLevel(LEVEL)
    logger.addHandler(console)

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
        '-s',
        '--sessions_path',
        action='store',
        default=SESSIONS_PATH,
        help='path/to/directory for save classified sessions .pcap file'
    )
    parser.add_argument(
        '-o',
        '--classified_only',
        action='store_true',
        default=False,
        help='displays classification result for classified sessions only'
    )
    parser.add_argument(
        '-d',
        '--disable_saving',
        action='store_true',
        default=False,
        help='disable classified sessions saving'
    )
    parser.add_argument(
        '-a',
        '--analyze',
        action='store_true',
        default=False,
        help='work in session analyzer mode. displaying sessions params only'
    )
    args = parser.parse_args()

    config = Config(args.config_file)
    config_params = config.classification_params
    dump = Dump(args.input_file)
    sessions = dump.get_all_sessions()
    for session_name, session_packets in sessions.items():
        classificator = Classificator(session_name, session_packets)
        session_params = classificator.get_session_params()
        if args.analyze:
            logger.info(f'{session_name}: {session_params}')
            continue
        result = classificator.classify_session(config_params, session_params)
        if args.classified_only:
            if result[0]:
                logger.info(result[1])
        else:
            logger.info(result[1])
        if result[0] and not args.disable_saving:
            saved_session_path = dump.save_session(session_packets, result[2], args.sessions_path)
            logger.info(f'Session {session_name} saved in {saved_session_path}')
