from classificator import Classificator

dr = Classificator('dumps/telegram_audio_common_flow.pcapng', 'configs/classificator.yml')
# dr.session_processing()
new = dr.get_protocol_sessions('UDP')
print(new)
print(dr.config)
session = dr.get_protocol_sessions('UDP')
dr.get_session_parameters(session)
