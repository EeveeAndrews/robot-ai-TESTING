from engine.state_machine import handle_awaiting_farewell_confirmation
from engine.classifier import classify_and_respond

def process_input(user_input, session):
    if session.current_state == "AWAITING_FAREWELL_CONFIRMATION":
        response = handle_awaiting_farewell_confirmation(
            user_input, session.state_entered_at
        )
    else:
        response = classify_and_respond(user_input, session)

    session.current_state = response["state"]
    session.state_entered_at = time.time()
    return response