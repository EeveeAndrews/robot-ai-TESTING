Comments are not supported in .json files, so any comments to the code written there are included in this file.

All separate intent JSON files are organized under one intents folder for ease of access. The software will be able to open them via load_all_files("intents/") rather than trying to access each individual file. Therefore, for ease of adding new files and editing existing ones, this is what I determined to be the best route.

Confidence intervals, frequently listed as "minimum_confidence", must be kept as high as reasonable depending on the kind of command. For example, accessing classified information and executing a hug/adjusting the hug strength should have high confidence values. These are set by the AI and range anywhere from 0 to 1.00.

The example verification methods in response_schema.json will likely be narrowed down to one or two. An array of some viable methods are listed regardless.

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

Python files are located in the "engine" folder. The rest of the .json files are essentially the pieces of data and alone are not sufficient to semi-train an AI model. 


-Intent descriptions-

protected_data_access.json regards a range of subject topics inclusive of both PII (Personally Identifiable Information) and PHI (Protected Health Information) if the user has stored it to the robot.

hug.json, as the name suggests, is an intent when the AI believes the user is requesting a hug or may want to have one. Various states are attributed to levels of uncertainty, that is, the AI will not immediately go into a hug if the user has only said "I've been feeling lonely". It will, however, move from each state to the next depending on further conversation in this scenario, ultimately ending with an execution of the hug command or a cancellation and reversion of the intent into a conversation or the end of one.

greeting.json is the intent when the AI believes the user is attempting to begin a conversation when one had not been taking place prior. It likely leads to the beginning of a conversation intent, but it still has the potential to abrupty trigger a farewell. 

conversation.json is nearly all-encompassing of any enagement with the user after a greeting has initiated and exclusive of an attempt to access protected information. "Topics" are subject to change or addition, but a few example ones present now are "trivia", "small_talk", and "entertainment". Rather than have separate .json files for each conversation topic, the one conversation.json is written accompanied by a list of possible topics the user may bring up to better guide them to one sort of answer.

farewell.json is the intent once, after initiating a conversation with the AI, the user indicates they would like to end the discussion. 

emergency.json is an emergency intent NOT ACCOUNTABLE for preventing injuries during any command execution. This is important because despite its existence, there should still be strong backup measures in place, such as strength limitations, in order to prevent harming the user at all costs. However, it is still very useful for reaching out for help for the user in hospital and assisted-living settings. When any indication of pain, struggle, or harm is detected by the AI, it is trained by the emergency.json file to handle it accordingly. Again, this is NOT responsible for the robot's safety protocols when engaging in a hug or other motor commands.

-Prompts Description- 

safety_prompt.md, as the name suggests,

system_prompt.md can be though of as a brief gateway into the AI's fabricated personality. It is what it can read to get a refined understanding of itself, its purpose, and what kind of demeanor it should adapt especially when engaging in conversation with the user. 

-Schemas Description-
Before reading, schemas essentially set up the framework for the information that intent .json files provide and what kind of output the module should give after processing user-input. Combined with schemas, the AI will understand the data type of certain variables I have chosed. For example, "description" is set up in the schema to be a string datatype and it is defined as a brief summary of an intent.

intent_schema.json tells the AI how to comprehend the intent files. As explained earlier, the "description" is a value present in each intent .json file, and this schema's job is to not only give a corresponding data type to this variable but also define it simply for the AI to digest.

response_schema.json, on the other hand, is the framework for how the AI will create output. This could include a command, speech in the form of a string, or a mix of the two. Additionally, it gives the module a chance to update memories, provide a confidence interval (see earlier definition), change its current state (i.e., conversation to idle), and a few other actions after it has processed BOTH user-input and the intent.json files we have provided for it to understand its purpose.