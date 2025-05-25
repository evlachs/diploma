from classificator import Classificator
from config_handler import Config
from dump_handler import Dump
from datetime import datetime


if __name__ == '__main__':
    start = datetime.now()
    config = Config('configs/services.yml')
    dump = Dump('dumps/telegram_audio_common_flow.pcapng')
    config_params = config.classification_params
    sessions = dump.get_all_sessions()
    for session_name, session_packets in sessions.items():
        classificator = Classificator(session_name, session_packets)
        session_params = classificator.get_session_params()
        result = classificator.classify_session(config_params, session_params)
        print(result)
    end = datetime.now()
