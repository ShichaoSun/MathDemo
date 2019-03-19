from flask import Flask, redirect, render_template, request
import json

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/result', methods=('POST', 'GET'))
def result():
    prob = request.form['prob']
    return str(prob)
#     if form.validate_on_submit():
#         s=form.q.data.split()
#         #results=doesnt_match(s)
#         results=model.most_similar(positive=[s[0],s[2]], negative=[s[1]])
#         return render_template("result.html",form=form,result=results)
#     else:
#         return redirect('/index')


@app.route('/success')
def success():
    t = '{0 [label=&#x22;&#xD7;&#x22;];1 [label=&#x22;&#xF7;&#x22;];2 [label=&#x22;&#xF7;&#x22;];3 [label=&#x22;1&#x22;];4 [label=&#x22;2&#x22;];5 [label=&#x22;0.62&#x22;];6 [label=&#x22;(5/5)&#x22;];0 -- 1 -- 2 -- 3; 2 -- 4; 1 -- 5; 0 --6}'

    # t = '{&#x22;&#xD7;&#x22; -- &#x22;&#xF7;&#x22; -- &#x22;0.54&#x22;;&#x22;&#xF7;&#x22; -- &#x22;2.5&#x22;; &#x22;&#xD7;&#x22; -- &#x22;(1/5)&#x22;; }'
    return render_template("success.html", t=t)


if __name__ == '__main__':
    app.run()
