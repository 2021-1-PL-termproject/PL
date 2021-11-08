var canvas = document.getElementById("response-prob");
var ctx = canvas.getContext("2d");
var width = 300;
var height = 40;
var radius = 20;

drawGraph();

function getFirst(){
    return prob1;
}

function getSecond(){
    return prob2;
}

function getThird(){
    return prob3;
}

function drawGraph(){
    var first = getFirst();
    var second = getSecond();
    var third = getThird();

    // first bar
    ctx.beginPath();
    ctx.arc(radius, radius, radius, 0.5*Math.PI, 1.5*Math.PI, false);
    ctx.moveTo(radius, 0);
    ctx.lineTo(first*width - radius, 0);
    ctx.arc(first*width - radius, radius, radius, 1.5*Math.PI, 0.5*Math.PI, false);
    ctx.moveTo(first*width - radius, height);
    ctx.lineTo(radius, height);
    ctx.lineTo(radius, 0);
    ctx.fillStyle = "gray";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.font = '12px malgun gothic'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = "black";
    ctx.fillText(parseInt(first*100) + "%", first*width + 10, radius);
    ctx.closePath();

    // second bar
    ctx.beginPath();
    ctx.arc(radius, 55 + radius, radius, 0.5*Math.PI, 1.5*Math.PI, false);
    ctx.moveTo(radius, 55);
    ctx.lineTo(second*width - radius, 55);
    ctx.arc(second*width - radius, 55 + radius, radius, 1.5*Math.PI, 0.5*Math.PI, false);
    ctx.moveTo(second*width - radius, 55 + height);
    ctx.lineTo(radius, 55 + height);
    ctx.lineTo(radius, 55);
    ctx.fillStyle = "gray";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.font = '12px malgun gothic'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = "black";
    ctx.fillText(parseInt(second*100) + "%", second*width + 10, 55+radius);
    ctx.closePath();

    // third bar
    ctx.beginPath();
    ctx.arc(radius, 110 + radius, radius, 0.5*Math.PI, 1.5*Math.PI, false);
    ctx.moveTo(radius, 110);
    ctx.lineTo(third*width - radius, 110);
    ctx.arc(third*width - radius, 110 + radius, radius, 1.5*Math.PI, 0.5*Math.PI, false);
    ctx.moveTo(third*width - radius, 110 + height);
    ctx.lineTo(radius, 110 + height);
    ctx.lineTo(radius, 110);
    ctx.fillStyle = "gray";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.font = '12px malgun gothic'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = "black";
    ctx.fillText(parseInt(third*100) + "%", third*width + 10, 110+radius);
    ctx.closePath();
}
