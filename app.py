from flask import Flask, jsonify, render_template_string
import math

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Time Complexity Visualizer</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body{
            margin:0;
            padding:20px;
            background:#f2f2f2;
            font-family:Arial,sans-serif;
        }

        .container{
            max-width:1000px;
            margin:auto;
            background:white;
            padding:20px;
            border-radius:10px;
            box-shadow:0 0 10px rgba(0,0,0,0.2);
            text-align:center;
        }

        h1{
            color:#333;
        }

        input[type=range]{
            width:80%;
        }

        canvas{
            margin-top:20px;
        }
    </style>
</head>

<body>

<div class="container">

<h1>Time Complexity Visualizer</h1>

<p>
Input Size (n):
<b id="value">20</b>
</p>

<input
type="range"
id="slider"
min="5"
max="100"
value="20">

<canvas id="chart"></canvas>

</div>

<script>

let chart;

async function updateChart(n){

document.getElementById("value").innerHTML=n;

const response=await fetch("/data/"+n);

const data=await response.json();

if(chart){
chart.destroy();
}

chart=new Chart(document.getElementById("chart"),{

type:"line",

data:{

labels:data.labels,

datasets:[

{
label:"O(1)",
data:data.o1,
borderColor:"red",
fill:false
},

{
label:"O(log n)",
data:data.ologn,
borderColor:"blue",
fill:false
},

{
label:"O(n)",
data:data.on,
borderColor:"green",
fill:false
},

{
label:"O(n log n)",
data:data.onlogn,
borderColor:"orange",
fill:false
},

{
label:"O(n²)",
data:data.on2,
borderColor:"purple",
fill:false
}

]

},

options:{
responsive:true
}

});

}

updateChart(20);

document.getElementById("slider").addEventListener("input",function(){
updateChart(this.value);
});

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/data/<int:n>")
def data(n):

    labels=list(range(1,n+1))

    o1=[1 for i in labels]

    ologn=[math.log2(i) if i>0 else 0 for i in labels]

    on=[i for i in labels]

    onlogn=[i*math.log2(i) if i>0 else 0 for i in labels]

    on2=[i*i for i in labels]

    return jsonify({
        "labels":labels,
        "o1":o1,
        "ologn":ologn,
        "on":on,
        "onlogn":onlogn,
        "on2":on2
    })

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
