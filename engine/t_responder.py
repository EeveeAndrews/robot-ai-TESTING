# engine/responder.py
def build_response(speech, next_state, intent="farewell", action=None, confidence=None):
    return {
        "intent": intent,
        "confidence": confidence,
        "speech": speech,
        "action": action,
        "state": next_state,
        "authenticated": None,
        "memory_update": None
}