var canvas = document.getElementById("response-prob");
var ctx = canvas.getContext("2d");
var width = canvas.width;
var height = 40;
var radius = 20;

//test
ctx.beginPath();
ctx.arc(75, 75, 20, 0.5*Math.PI, 1.5*Math.PI, false);
ctx.moveTo(75, 55);
ctx.lineTo(width, 55);
ctx.arc(width-20, 75, 20, 1.5*Math.PI, 0.5*Math.PI, false);
ctx.moveTo(width-20, 95);
ctx.lineTo(75, 95);
ctx.lineTo(75, 55);
ctx.fillStyle = "gray";
ctx.fill();
ctx.closePath();

// test
var a = getFirst();
ctx.beginPath();
ctx.font = "16px malgun gothic";
ctx.textBaseline = "middle";
ctx.textAlign = "left";
ctx.fillStyle = "black";
ctx.fillText(a, 30, 0);
ctx.fillText(typeof(a), 30, 20);
ctx.closePath();

var a = getFirst();
ctx.beginPath();
ctx.font = "16px malgun gothic";
ctx.textBaseline = "middle";
ctx.textAlign = "left";
ctx.fillStyle = "black";
ctx.fillText(a, 30, 0);
ctx.fillText(typeof(a), 30, 20);
ctx.closePath();

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

function getFirstName(){
    return prob11;
}

function getSecondName(){
    return prob21;
}

function getThirdName(){
    return prob31;
}

function drawGraph(){
    var first = getFirst();
    var second = getSecond();
    var third = getThird();
    var first_name = getFirstName();
    var second_name = getSecondName();
    var third_name = getThirdName();

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
    ctx.font = "16px malgun gothic";
    ctx.textBaseline = "middle";
    ctx.textAlign = "left";
    ctx.fillStyle = "black";
    ctx.fillText(first_name, first*width, 20);
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
    ctx.font = "16px malgun gothic";
    ctx.textBaseline = "middle";
    ctx.textAlign = "left";
    ctx.fillStyle = "black";
    ctx.fillText(second_name, second*width, 20);
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
    ctx.font = "16px malgun gothic";
    ctx.textBaseline = "middle";
    ctx.textAlign = "left";
    ctx.fillStyle = "black";
    ctx.fillText(third_name, third*width, 20);
    ctx.closePath();
}
