import os
import re
string st = ""

question_files = ['mentor_questions.txt', 'friend_questions.txt', 'partner_questions.txt']

for fname in question_files:
    file_path = f'./Questions/{fname}'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read().strip()
            content = content.strip('[')
            content = content.strip(']')
            content = content.strip('"')
            c = content.split(r'",( *)\n"')
            for s in c:
                st += s.strip()
                st += "\n"
        with open(file_path, 'w') as f:
            f.seek(0)
            f.write(st)
            
