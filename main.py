from classificator import Classificator
from config_handler import ConfigHandler
from dump_handler import DumpHandler

dump = DumpHandler('dumps/telegram_audio_common_flow.pcapng')
print(list(dump.get_all_sessions())[0].split()[0])

# if __name__ == '__main__':
#     config = ConfigHandler('configs/services.yml')
#
