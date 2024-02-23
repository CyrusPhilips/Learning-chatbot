import json
from difflib import SequenceMatcher

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_answer(question, knowledge_box):
    matched_question = None
    max_similarity = 0
    
    for category in knowledge_box['categories']:
        for item in category['questions']:
            similarity = similar(question.lower(), item['question'].lower())
            if similarity > max_similarity:
                matched_question = item
                max_similarity = similarity
    
    if matched_question and max_similarity >= 0.5:
        return matched_question['answer']
    else:
        return None

def main():
    data_file = 'C:/Users/HP/OneDrive/Pictures/Screenshots/College/Projects/Learning Chatbot/knowlege_box.json'
    knowledge_box = load_data(data_file)
    if knowledge_box is None:
        return

    exit_keywords = ['Goodbye', 'bye', 'Ohk then']

    while True:
        user_input = input("You: ").strip().lower()
        if user_input in exit_keywords:
            print("Goodbye!")
            break
        
        answer = get_answer(user_input, knowledge_box)
        if answer:
            print("LB:", answer)
        else:
            print("LB: I don't know the answer to that question.")
            teach_me = input("LB: Can you teach me or skip? (yes/no): ").strip().lower()
            if teach_me == 'yes':
                new_question = user_input
                new_answer = input("LB: What's the answer to that question? ").strip()
                knowledge_box['categories'][0]['questions'].append({"question": new_question, "answer": new_answer})
                save_data(data_file, knowledge_box)
                print("LB: Thanks for teaching me!")
            else:
                print("LB: Okay, ask me something else.")

if __name__ == "__main__":
    main()