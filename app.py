from flask import Flask, render_template, request
from mathsolver.pre_data import *
from mathsolver.predict import *

batch_size = 64
embedding_size = 128
hidden_size = 512
n_epochs = 80
learning_rate = 1e-3
weight_decay = 1e-5
beam_size = 5
n_layers = 2

data = load_raw_data("static/data/Math_23K.json")
pairs, generate_nums, copy_nums = transfer_num(data)
temp_pairs = []
for p in pairs:
    temp_pairs.append((p[0], from_infix_to_prefix(p[1]), p[2], p[3]))
pairs = temp_pairs

input_lang, output_lang = prepare_data(pairs, 5, generate_nums, copy_nums, tree=True)
# Initialize models
encoder = EncoderSeq(input_size=input_lang.n_words, embedding_size=embedding_size, hidden_size=hidden_size,
                     n_layers=n_layers)
predict = Prediction(hidden_size=hidden_size, op_nums=output_lang.n_words - copy_nums - 1 - len(generate_nums),
                     input_size=len(generate_nums))
generate = GenerateNode(hidden_size=hidden_size, op_nums=output_lang.n_words - copy_nums - 1 - len(generate_nums),
                        embedding_size=embedding_size)
merge = Merge(hidden_size=hidden_size, embedding_size=embedding_size)

encoder.load_state_dict(torch.load("static/models/encoder"))
predict.load_state_dict(torch.load("static/models/predict"))
generate.load_state_dict(torch.load("static/models/generate"))
merge.load_state_dict(torch.load("static/models/merge"))

# Move models to GPU
if USE_CUDA:
    encoder.cuda()
    predict.cuda()
    generate.cuda()
    merge.cuda()

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
    seq, nums, num_pos = pre_sent(prob, input_lang.word2index)
    out = evaluate_tree(seq, len(seq), generate_nums, encoder, predict, generate, merge, output_lang, num_pos)

    out_seq = out_expression_list(out, output_lang, nums)
    ans = compute_prefix_expression(out_seq)

    exp, tree = generate_exp_tree(out_seq)

    ans = "%.2f" % ans

    if ans[-3:] == ".00":
        ans = ans[:-3]
    exp += "=" + ans
    return render_template("result.html", prob=prob, tree=tree, exp=exp)


if __name__ == '__main__':
    app.run()
