import time
from engine.t_state_machine import (
    handle_awaiting_farewell_confirmation,
    handle_authentication_required,
    handle_access_granted,
    handle_access_denied,
)
from engine.t_classifier import classify_and_respond

STATE_HANDLERS = {
    "AWAITING_FAREWELL_CONFIRMATION": handle_awaiting_farewell_confirmation,
    "AUTHENTICATION_REQUIRED": handle_authentication_required,
    "ACCESS_GRANTED": handle_access_granted,
    "ACCESS_DENIED": handle_access_denied,
}


def process_input(user_input, session):
    handler = STATE_HANDLERS.get(session.current_state)

    if handler:
        response = handler(user_input, session.state_entered_at)
    else:
        response = classify_and_respond(user_input, session)

    # hug's next_state is null by design -- stay in whatever state we were in
    session.current_state = response["state"] or session.current_state
    session.state_entered_at = time.time()
    return response