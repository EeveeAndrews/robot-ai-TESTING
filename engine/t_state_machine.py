import re
import time
from engine.t_responder import build_response

YES_PATTERN = re.compile(r"\b(yes|yeah|yep|sure|please|go ahead|okay|ok)\b", re.IGNORECASE)
NO_PATTERN = re.compile(r"\b(no|nope|not yet|nah|don't|actually)\b", re.IGNORECASE)
CONFIRMATION_TIMEOUT_SECONDS = 15


def handle_awaiting_farewell_confirmation(user_input, state_entered_at):
    elapsed = time.time() - state_entered_at

    if elapsed > CONFIRMATION_TIMEOUT_SECONDS:
        return build_response(speech=None, next_state="CONVERSATION_ONGOING", intent="farewell")

    if YES_PATTERN.search(user_input):
        return build_response(
            speech="Goodnight! I'll be here when you want to talk again.",
            next_state="IDLE",
            intent="farewell"
        )

    if NO_PATTERN.search(user_input):
        return build_response(
            speech="Okay, glad you're sticking around!",
            next_state="CONVERSATION_ONGOING",
            intent="farewell"
        )

    return build_response(
        speech="No worries, we can keep chatting.",
        next_state="CONVERSATION_ONGOING",
        intent="farewell"
    )


def run_authentication_check():
    """Bare-bones stub: no real biometric hookup yet, always fails."""
    return False


def handle_authentication_required(user_input, state_entered_at):
    auth_result = run_authentication_check()

    if auth_result is None:
        return build_response(speech=None, next_state="AUTHENTICATION_REQUIRED", intent="classified_access")

    if auth_result:
        return build_response(
            speech="__RETRIEVED_FROM_MEMORY__",
            next_state="ACCESS_GRANTED",
            intent="classified_access",
            action={"action_type": "ACCESS_CLASSIFIED_DATA"},
            authenticated=True
        )

    return build_response(
        speech="I'm sorry, I could not verify your identity. I cannot access your information at this time.",
        next_state="ACCESS_DENIED",
        intent="classified_access",
        action={"action_type": "ACCESS_DENIED"},
        authenticated=False
    )


def handle_access_granted(user_input, state_entered_at):
    return build_response(speech=None, next_state="CONVERSATION_ONGOING", intent="classified_access")


def handle_access_denied(user_input, state_entered_at):
    return build_response(speech=None, next_state="CONVERSATION_ONGOING", intent="classified_access")