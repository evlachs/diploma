from classificator import Classificator

dr = Classificator('dumps/telegram_audio_common_flow.pcapng', 'configs/services.yml')
all_sessions = dr.get_protocol_sessions('UDP')

for session_name, session in all_sessions.items():
    params = dr.get_session_params('udp', session)
    classification = dr.check_session_affiliation(session_name, params)
    if classification[0]:
        print(classification[1])
