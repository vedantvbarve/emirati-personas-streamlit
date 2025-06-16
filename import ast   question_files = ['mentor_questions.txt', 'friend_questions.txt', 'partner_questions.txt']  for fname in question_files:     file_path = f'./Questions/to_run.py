import ast 

question_files = ['mentor_questions.txt', 'friend_questions.txt', 'partner_questions.txt']

for fname in question_files:
    file_path = f'./Questions/{fname}'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        # Check if it looks like a Python list
        if content.startswith('[') and content.endswith(']'):
            try:
                arr = ast.literal_eval(content)
                if isinstance(arr, list):
                    # Overwrite with plain text, one question per line
                    with open(file_path, 'w', encoding='utf-8') as f:
                        for q in arr:
                            f.write(q.strip() + '\n')
            except Exception:
                pass  # If it fails, do nothing 
