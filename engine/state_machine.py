import re
import time

YES_PATTERN = re.compile(r"\b(yes|yeah|yep|sure|please|go ahead|okay|ok)\b", re.IGNORECASE)
NO_PATTERN = re.compile(r"\b(no|nope|not yet|nah|don't|actually)\b", re.IGNORECASE)
CONFIRMATION_TIMEOUT_SECONDS = 15

def handle_awaiting_farewell_confirmation(user_input, state_entered_at):
    elapsed = time.time() - state_entered_at

    if elapsed > CONFIRMATION_TIMEOUT_SECONDS:
        return build_response(
            speech=None,
            next_state="CONVERSATION_ONGOING"
        )

    if YES_PATTERN.search(user_input):
        return build_response(
            speech="Goodnight! I'll be here when you want to talk again.",
            next_state="IDLE"
        )

    if NO_PATTERN.search(user_input):
        return build_response(
            speech="Okay, glad you're sticking around!",
            next_state="CONVERSATION_ONGOING"
        )

    return build_response(
        speech="No worries, we can keep chatting.",
        next_state="CONVERSATION_ONGOING"
    )

# def handle_awaiting_hug_confirmation(user_input, state_entered_at):
#     ...

# def handle_waiting_authentication(user_input, state_entered_at):
#     ...

# def handle_waiting_authentication(user_input, state_entered_at):
#     ...

# def handle_waiting_authentication(user_input, state_entered_at):
#     ...

# engine/state_machine.py (additions)

def handle_authentication_required(user_input, state_entered_at):
    """
    State entered after protected_data_access.json's 'request' behavior fires.
    Doesn't parse user_input -- triggers the actual auth check instead.
    """
    auth_result = run_authentication_check()  # returns True / False / None (still working)

    if auth_result is None:
        # still verifying, e.g. camera/mic still processing -- stay in this state
        return build_response(
            speech=None,
            next_state="AUTHENTICATION_REQUIRED",
            intent="classified_access"
        )

    if auth_result:
        return build_response(
            speech="__RETRIEVED_FROM_MEMORY__",  # responder.py resolves this, see note below
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
    """
    Transient state -- access was already granted and spoken last turn.
    Immediately falls back to normal conversation on the next input.
    """
    return build_response(
        speech=None,
        next_state="CONVERSATION_ONGOING",
        intent="classified_access"
    )


def handle_access_denied(user_input, state_entered_at):
    """
    Transient state -- denial was already spoken last turn.
    Immediately falls back to normal conversation on the next input.
    """
    return build_response(
        speech=None,
        next_state="CONVERSATION_ONGOING",
        intent="classified_access"
    )