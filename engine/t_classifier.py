import re
import random
from engine.t_loader import load_all_intents
from engine.t_responder import build_response

INTENTS = load_all_intents()


def _tokenize(text):
    # strip punctuation, lowercase -- fixes "Hello!" vs "Hello." mismatch
    return re.findall(r"[a-z0-9']+", text.lower())


def _score(user_input, example_text):
    user_words = set(_tokenize(user_input))
    example_words = set(_tokenize(example_text))
    if not example_words or not user_words:
        return 0.0
    overlap = user_words & example_words
    # average of two ratios so short examples don't get an unfair boost
    precision = len(overlap) / len(example_words)
    recall = len(overlap) / len(user_words)
    return (precision + recall) / 2


def _best_match(user_input):
    best_intent, best_topic, best_score = None, None, 0.0
    for intent_name, data in INTENTS.items():
        for example in data["examples"]:
            score = _score(user_input, example["text"])
            if score > best_score:
                best_score = score
                best_intent = intent_name
                best_topic = example.get("topic")
    return best_intent, best_topic, best_score


def _pick_behavior_state(data, topic):
    behavior = data["behavior"]
    if "responses" in behavior:
        return behavior
    if topic and topic in behavior:
        return behavior[topic]
    return next(iter(behavior.values()))


def classify_and_respond(user_input, session):
    intent_name, topic, score = _best_match(user_input)

    if intent_name is None:
        return build_response(speech=None, next_state=session.current_state, intent="none")

    data = INTENTS[intent_name]
    min_confidence = data.get("security", {}).get("minimum_confidence", 0.0)

    if score < min_confidence:
        if session.current_state == "CONVERSATION_ONGOING":
            return build_response(
                speech="That's great to hear! Tell me more.",
                next_state="CONVERSATION_ONGOING",
                intent="conversation",
                confidence=score
            )
        return build_response(speech=None, next_state=session.current_state, intent="none", confidence=score)

    state = _pick_behavior_state(data, topic)

    return build_response(
        speech=random.choice(state["responses"]),
        next_state=state.get("next_state") or session.current_state,
        intent=intent_name,
        action=state.get("action"),
        confidence=score
    )