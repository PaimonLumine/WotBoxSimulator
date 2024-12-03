import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# 定义概率和奖励
rewards = [
    ("装饰物", 0.25),
    ("SU-100I", 0.1166/5),
    ("38(K)", 0.1166/5),
    ("二式炮战车", 0.1166/5),
    ("M3A3 斯图亚特", 0.1166/5),
    ("AMR P.103", 0.1166/5),
    ("高级账号天数1", 0.8594/9),
    ("高级账号天数3", 0.8594/9),
    ("高级账号天数7", 0.8594/9),
    ("金币250", 0.8594/9),
    ("金币500", 0.8594/9),
    ("金币1000", 0.8594/9),
    ("银币100000", 0.8594/6),
    ("银币500000", 0.8594/6),
    ("DZT-159", 0.024/5),
    ("金牛座", 0.024/5),
    ("XM57", 0.024/5),
    ("Vz.68 S", 0.024/5),
    ("FV226 反制者", 0.024/5),
    ("3D风格", 0.05),
    ("全新3D附件", 0.06)
]

# 定义坦克及其金币补偿
tank_compensation = {
    "DZT-159": 11900,
    "金牛座": 12450,
    "FV226 反制者": 10200,
    "XM57": 9400,
    "Vz.68 S": 6500,
    "SU-100I": 1500,
    "38(K)": 1300,
    "二式炮战车": 950,
    "M3A3 斯图亚特": 500,
    "AMR P.103": 500
}

# 追踪已获得的坦克
obtained_tanks = set()
unique_tanks = {"DZT-159", "金牛座", "FV226 反制者", "XM57", "Vz.68 S"}

# 记录每种坦克的获得次数
tank_counts = {tank: 0 for tank in tank_compensation}

# 保底计数器
pity_counter = 0

# 模拟掉落函数
def simulate_drop():
    global obtained_tanks, pity_counter
    pity_counter += 1

    # 保底机制
    if pity_counter >= 50:
        for tank in unique_tanks:
            if tank not in obtained_tanks:
                obtained_tanks.add(tank)
                pity_counter = 0
                return tank

    while True:
        drop = random.choices(rewards, weights=[r[1] for r in rewards], k=1)[0][0]
        if drop in unique_tanks and drop in obtained_tanks:
            continue
        if drop in unique_tanks:
            obtained_tanks.add(drop)
            pity_counter = 0
        return drop

# HTML模板
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>假日行动2025 掉落模拟器</title>
    <style>
        .container {
            display: flex;
        }
        .main {
            flex: 3;
        }
        .sidebar {
            flex: 1;
            padding-left: 20px;
        }
        .fixed-sidebar {
            position: fixed;
            right: 0;
            top: 0;
            width: 20%;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main">
            <h1>假日行动2025 掉落模拟器</h1>
            <p>点击按钮来模拟一次掉落:</p>
            <form method="post">
                <button type="submit" name="drop" value="1">模拟掉落</button>
                <button type="submit" name="drop" value="10">模拟掉落10次</button>
            </form>
            {% if reward %}
                <h2>掉落结果: {{ reward }}</h2>
            {% endif %}
            <h2>掉落记录</h2>
            <ul>
                {% for record in records %}
                    <li>{{ record }}</li>
                {% endfor %}
            </ul>
        </div>
        <div class="sidebar fixed-sidebar">
            <h2>统计信息</h2>
            <p>总掉落次数: {{ total_drops }}</p>
            <p>累计获得金币: {{ total_gold }}</p>
            <p>累计获得银币: {{ total_silver }}</p>
            <p>累计获得高级账号天数: {{ total_premium_days }}</p>
            <h2>获得的坦克</h2>
            <ul>
                {% for tank, count in tank_counts.items() %}
                    <li>{{ tank }}: {{ count }} 次</li>
                {% endfor %}
            </ul>
        </div>
    </div>
</body>
</html>
"""

drop_records = []
total_drops = 0
total_gold = 0
total_silver = 0
total_premium_days = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global total_drops, total_gold, total_silver, total_premium_days
    reward = None
    if request.method == "POST":
        drop_count = int(request.form.get("drop", 1))
        for _ in range(drop_count):
            reward = simulate_drop()
            drop_records.append(reward)
            if reward in tank_compensation:
                if reward in obtained_tanks:
                    total_gold += tank_compensation[reward]
                tank_counts[reward] += 1
            elif reward.startswith("金币"):
                total_gold += int(reward[2:])
            elif reward.startswith("银币"):
                total_silver += int(reward[2:])
            elif reward.startswith("高级账号天数"):
                total_premium_days += int(reward[6:])
        total_drops += drop_count
    return render_template_string(html_template, reward=reward, records=drop_records, total_drops=total_drops, total_gold=total_gold, total_silver=total_silver, total_premium_days=total_premium_days, tank_counts=tank_counts)

if __name__ == "__main__":
    app.run(debug=True)