from flask import Flask, render_template, request
import json

app = Flask(__name__)

def parse_uploaded_file(file):
    content = file.read().decode('utf-8')
    # 先尝试逐行解析，判断是否为 JSONL 格式
    lines = content.strip().splitlines()
    data = []
    is_jsonl = True
    for line in lines:
        try:
            obj = json.loads(line)
            data.append(obj)
        except json.JSONDecodeError:
            is_jsonl = False
            break
    if is_jsonl and data:
        return data
    # 如果不是 JSONL，则尝试整体解析为 JSON 对象
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    error = None
    if request.method == 'POST':
        if 'file' not in request.files:
            error = "没有文件上传"
        else:
            file = request.files['file']
            if file.filename == '':
                error = "没有选择文件"
            else:
                data = parse_uploaded_file(file)
                if data is None:
                    error = "无法解析上传的文件，请确保文件是有效的 JSON 或 JSONL 格式"
    return render_template('index.html', data=data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
