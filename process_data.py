import json
import csv

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def process_messages(messages):
    result = []

    for eachChat in messages:
        eachChat = eachChat["messages"]

        for eachMessage in eachChat:
            # Skip the message if 'from' key doesn't exist
            if "from" not in eachMessage:
                continue

            name = eachMessage["from"]

            # Handle different types of 'text' field
            if "text" in eachMessage and len(eachMessage["text"]) > 0:
                if isinstance(eachMessage["text"], str):
                    text = eachMessage["text"]
                elif isinstance(eachMessage["text"], list):
                    text = " ".join(str(item) for item in eachMessage["text"])
                else:
                    text = str(eachMessage["text"])
            elif "sticker_emoji" in eachMessage:
                text = eachMessage["sticker_emoji"]
            else:
                continue

            # Add each message as a separate row
            result.append([name, text])

    return result


def write_csv(data, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "list"])
        writer.writerows(data)


def main():
    input_file = "result.json"  # Replace with your JSON file path
    output_file = "telegram_chat.csv"  # Output CSV file name

    json_data = load_json(input_file)
    chats_data = json_data["chats"]["list"]
    processed_data = process_messages(chats_data)
    write_csv(processed_data, output_file)

    print(f"CSV file '{output_file}' has been created successfully.")


if __name__ == "__main__":
    main()
