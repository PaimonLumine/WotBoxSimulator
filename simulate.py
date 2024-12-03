import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# 定义概率和奖励
rewards = [
    ("装饰物", 0.25),
    ("低等级金币坦克", 0.1166),
    ("高级账号天数", 0.8594/3),
    ("金币", 0.8594/3),
    ("银币", 0.8594/3),
    ("DZT-159", 0.024/5),
    ("金牛座", 0.024/5),
    ("XM57", 0.024/5),
    ("VZ68S", 0.024/5),
    ("FV226", 0.024/5),
    ("3D风格", 0.05),
    ("全新3D附件", 0.06)
]

# 模拟掉落函数
def simulate_drop():
    drop = random.choices(rewards, weights=[r[1] for r in rewards], k=1)
    return drop[0][0]

# HTML模板
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>假日行动2025 掉落模拟器</title>
</head>
<body>
    <h1>假日行动2025 掉落模拟器</h1>
    <p>点击按钮来模拟一次掉落:</p>
    <form method="post">
        <button type="submit">模拟掉落</button>
    </form>
    {% if reward %}
        <h2>掉落结果: {{ reward }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    reward = None
    if request.method == "POST":
        reward = simulate_drop()
    return render_template_string(html_template, reward=reward)

if __name__ == "__main__":
    app.run(debug=True)
