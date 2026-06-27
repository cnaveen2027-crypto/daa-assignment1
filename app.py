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
            font-family:Arial, sans-serif;
            background:#f5f5f5;
            text-align:center;
            margin:0;
            padding:30px;
        }

        .container{
            max-width:1000px;
            margin:auto;
            background:white;
            padding:20px;
            border-radius:10px;
            box-shadow:0 0 10px rgba(0,0,0,.2);
        }

        h2{
            color:#333;
        }

        #slider{
            width:80%;
            margin-top:15px;
        }

        #value{
            font-weight:bold;
            color:blue;
        }

        canvas{
            margin-top:30px;
        }
    </style>
</head>

<body>

<div class="container">

<h2>Time Complexity Visualizer</h2>

<p>
Select n :
<span id="value">20</span>
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

async function loadData(n){

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
                data:data["O(1)"],
                borderColor:"red",
                fill:false
            },

            {
                label:"O(log n)",
                data:data["O(log n)"],
                borderColor:"blue",
                fill:false
            },

            {
                label:"O(n)",
                data:data["O(n)"],
                borderColor:"green",
                fill:false
            },

            {
                label:"O(n log n)",
                data:data["O(n log n)"],
                borderColor:"orange",
                fill:false
            },

            {
                label:"O(n²)",
                data:data["O(n²)"],
                borderColor:"purple",
                fill:false
            }

            ]

        },

        options:{

            responsive:true,

            plugins:{
                legend:{
                    position:"top"
                }
            }

        }

    });

}

loadData(20);

document.getElementById("slider").addEventListener("input",function(){
    loadData(this.value);
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

    x=list(range(1,n+1))

    o1=[1 for i in x]

    ologn=[math.log2(i) for i in x]

    on=[i for i in x]

    onlogn=[i*math.log2(i) for i in x]

    on2=[i*i for i in x]

    return jsonify({

        "labels":x,

        "O(1)":o1,

        "O(log n)":ologn,

        "O(n)":on,

        "O(n log n)":onlogn,

        "O(n²)":on2

    })


if __name__=="__main__":
    app.run(debug=True)
