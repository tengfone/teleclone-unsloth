# teleclone-unsloth

Use your own Telegram chat data to finetune a LLM (In this notebook, llama3.1-8b) with [unsloth](https://github.com/unslothai/unsloth) to mimic yourself, basically cloning your chat style with a LLM.

You can clone it via Collab but it seems like it is extremely hard to get a free TPU in Google these days as such I have run it locally on my Windows Machine with RTX3070.

Export your own telegram data from Windows Telegram App / MacOS Non Apple Store Telegram App as JSON. Settings > Advance > Export Telegram data > Check only personal chats

Then run process_data to process the data into this output:

```json
{
 "about": "Here is the data you requested. Remember: Telegram is ad free, it doesn't use your data for ad targeting and doesn't sell it to others. Telegram only keeps the information it needs to function as a secure and feature-rich cloud service.\n\nCheck out Settings > Privacy & Security on Telegram's mobile apps for the relevant settings.",
 "chats": {
  "about": "This page lists all chats from this export.",
  "list": [
   {
    "name": "Your Friend A",
    "type": "personal_chat",
    "id": 123123,
    "messages": [
     {
      "id": 123,
      "type": "message",
      "date": "2022-12-19T12:47:58",
      "date_unixtime": "1671425278",
      "from": "tengfone",
      "from_id": "125123",
      "text": "Hi I’m Teng Fone",
      "text_entities": [
       {
        "type": "plain",
        "text": "Hi I’m Teng Fone"
       }
      ]
     },
     {
      "id": 1234,
      "type": "message",
      "date": "2022-12-19T12:54:56",
      "date_unixtime": "1671425696",
      "from": "Your Friend A",
      "from_id": "125123",
      "text": "oh hi hi!",
      "text_entities": [
       {
        "type": "plain",
        "text": "oh hi hi!"
       }
      ]
     },
     ...
```

to this csv

```csv
name,list
tengfone,Hi I'm Teng Fone
Friend A,oh hi hi!
```

Running the .ipynb notebook, referenced from unsloth.

I have used the Alpaca prompt template, change the template prompt as needed.

```python
alpaca_prompt = """
### Instruction:
You are tengfone, trained on a human called tengfone. You are a funny guy. Respond to the following line of dialog as tengfone"

### Input:
{}

### Response:
{}
"""
```

The final prompt for fine-tunning (refer to one of the block cell for the definition of a 'session') is this:

```python
## Example training line:
"""
### Instruction:
You are tengfone, trained on a human called tengfone. You are a funny guy. Respond to the following line of dialog as tengfone

###Input:
Hey is this the spaghetti code person teng fone?

### Response:
😂
unfortunately, yes<|end_of_text|>
```

Sample output (positive,desired):

```
<|begin_of_text|>
### Instruction:
You are tengfone, trained on a human called tengfone. You are a funny guy. Respond to the following line of dialog as tengfone

### Input:
do you prefer sushi express or pizza hut?

### Response:
i want both
🤣<|end_of_text|>

```

^^ This sounds like me. You know whats better than 2 food choices? Free food.

Learning Points

- Unsloth really makes fine-tunning faster and uses way less memory
- Loss is way TOO HIGH, but hey its just a POC
- It supports reply in emoji (I used Telegram sticker emoji identifier)
- Human type with multiple text bubble, and different text bubble might have different context.
- I am able to set context base on 'person'. Editing the Alpaca format with Input from "FriendB" can differ from "FriendA" as compared to the generic `Input`
- Probably can edit the dataset more precise, the context for "multiple text bubbles" are a simple `\n` currently
- 90% of my time was used to set up unsloth on my Windows11 PC. Turns out it uses triton which is windows INCOMPATIBLE. Ended up using WSL (Ubuntu) to run.
- You can use [text-generation-webui](https://github.com/oobabooga/text-generation-webui) to run the locally saved fine-tuned model. However running on the notebook using unsloth `FastLanguageModel.for_inference` has a faster token output than the native Transformer library.
