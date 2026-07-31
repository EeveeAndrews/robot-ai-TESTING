Comments are not supported in .json files, so any comments to the code written there are included in this file.

All separate intent JSON files are organized under one intents folder for ease of access. The software will be able to open them via load_all_files("intents/") rather than trying to access each individual file. Therefore, for ease of adding new files and editing existing ones, this is what I determined to be the best route.

Confidence intervals, frequently listed as "minimum_confidence", must be kept as high as reasonable depending on the kind of command. For example, accessing classified information and executing a hug/adjusting the hug strength should have high confidence values. These are set by the AI and range anywhere from 0 to 1.00.

The example verification methods in response_schema.json will likely be narrowed down to one or two. An array of some viable methods are listed regardless.

I should split conversation.json up into different categories, i.e., entertainment, reminiscing/memories(?), small_talk, etc. 

An example of how GPT may repons with JSON given response_schema.json:

User: "I'm feeling lonely."

GPT:
{
    "intent": "hug",
    "confidence": 0.94,
    "speech": "I'm sorry to hear you feel that way. Would you like a hug?",
    "action": null
    "state": "WAITING_FOR_HUG_CONFIRMATION",
    "memory_update": null
}

Note to self: use pathlib for Python.


-Intent descriptions-

protected_data_access.json is inclusive of both PII (Personally Identifiable Information) and PHI (Protected Health Information) if the user has stored it to the robot.

hug.json

greeting.json

emergency.json