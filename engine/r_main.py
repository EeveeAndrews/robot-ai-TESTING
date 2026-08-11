# # meow
# from engine.state_machine import handle_awaiting_farewell_confirmation
# from engine.state_machine import handle_awaiting_hug_confirmation
# from engine.classifier import classify_and_respond

# def process_input(user_input, session):
#     if session.current_state == "AWAITING_FAREWELL_CONFIRMATION":
#         response = handle_awaiting_farewell_confirmation(
#             user_input, session.state_entered_at
#         )
#     else:
#         response = classify_and_respond(user_input, session)

#     if session.current_state == "AWAITING_HUG_CONFIRMATION":
#         response = handle_awaiting_farewell_confirmation(
#              user_input, session.state_entered_at
#         )
#     else:
#         response = classify_and_respond(user_input, session)

#     session.current_state = response["state"]
#     session.state_entered_at = time.time()
#     return response


# engine/main.py
from engine.state_machine import (
    handle_awaiting_farewell_confirmation,
    handle_awaiting_hug_confirmation,
    handle_authentication_required,
    handle_access_granted,
    handle_access_denied,
)
from engine.classifier import classify_and_respond

STATE_HANDLERS = {
    "AWAITING_FAREWELL_CONFIRMATION": handle_awaiting_farewell_confirmation,
    "AWAITING_HUG_CONFIRMATION": handle_awaiting_hug_confirmation,
    "AUTHENTICATION_REQUIRED": handle_authentication_required,
    "ACCESS_GRANTED": handle_access_granted,
    "ACCESS_DENIED": handle_access_denied,
}

#  FORMAT FOR WRITING HANDLERS VVV

# def process_input(user_input, session):
#     handler = STATE_HANDLERS.get(session.current_state)

#     if handler:
#         response = handler(user_input, session.state_entered_at)
#     else:
#         # no special handler -- run normal intent classification
#         response = classify_and_respond(user_input, session)

#     session.current_state = response["state"]
#     session.state_entered_at = time.time()
#     return response