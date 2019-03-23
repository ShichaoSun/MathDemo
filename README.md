# Demo for Chinese Math Word Problem Solver

<img src="readme/index.png" align="center" width="700px">

<img src="readme/example_1.png" align="center" width="400px"> <img src="readme/example_2.png" align="center" width="400px">

## Run 
```
sudo python app.py
```

## Requirements
- Python 3.6
- Flask 1.0.2
- Jieba
- PyTorch 1.0

## Technical details
- [visjs](http://visjs.org/) to show the expression tree
- [he](https://github.com/mathiasbynens/he) to encode and decode HTML entity
- [DOT language](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) to describe tree which is drawn by visjs 

