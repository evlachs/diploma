from classificator import Classificator

dr = Classificator('dumps/telegram_audio_common_flow.pcapng', 'configs/classificator.yml')
print(dr.config)
session = dr.get_protocol_sessions('UDP')
dr.get_session_parameters(session)
