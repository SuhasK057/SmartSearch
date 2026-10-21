import re

with open('mock_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = re.sub(r'"likes":\s*\d+', '"likes": 0', content)

with open('mock_data.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated likes in mock_data.py to 0 successfully.")
