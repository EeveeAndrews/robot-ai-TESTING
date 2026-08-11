def build_response(speech, next_state, intent, action=None, confidence=None, authenticated=None):
    return {
        "intent": intent,
        "confidence": confidence,
        "speech": speech,
        "action": action,
        "state": next_state,
        "authenticated": authenticated,
        "memory_update": None
    }