from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    probs = [
        "黄瓜每千克的售价为3.20元，妈妈买了1.5千克黄瓜，应付多少元？",
        "一个工程队挖土，第一天挖了316方，从第二天开始每天都挖230方，连续挖了6天，这个工程队一周共挖土多少方？",
        "一个果园的李树棵数是桃树的(7/8)，桃树棵数是梨树的(5/6)．已知李树有1680棵，梨树有多少棵？"
    ]
    return render_template("index.html", probs=probs)


@app.route('/result', methods=('POST', 'GET'))
def result():
    prob = request.form['prob']
    tree = '{0 [label=&#x22;&#xD7;&#x22;];1 [label=&#x22;&#xF7;&#x22;];2 [label=&#x22;&#xF7;&#x22;];3 [label=&#x22;1&#x22;];4 [label=&#x22;2&#x22;];5 [label=&#x22;0.62&#x22;];6 [label=&#x22;(5/5)&#x22;];0 -- 1 -- 2 -- 3; 2 -- 4; 1 -- 5; 0 --6}'
    exp = "316+230×(6-1)=1466"
    return render_template("result.html", prob=prob, tree=tree, exp=exp)


if __name__ == '__main__':
    app.run()
