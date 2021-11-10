var canvas = document.getElementById("participation-days");
var ctx = canvas.getContext("2d");
var width = 300;
var height = 40;
var radius = 20;

drawGraph();

function getFirst(){
    return day1;
}

function getSecond(){
    return day2;
}

function getThird(){
    return day3;
}

function getOthers(){
    return day_others;
}

function drawGraph(){
    var first = getFirst();
    var second = getSecond();
    var third = getThird();
    var others = getOthers();

    var width1 = width;
    var width2 = (second / first) * width;
    var width3 = (third / first) * width;
    var width4 = (others / first) * width;

    // first bar
    ctx.beginPath();
    ctx.arc(radius, radius, radius, 0.5*Math.PI, 1.5*Math.PI, false);
    ctx.moveTo(radius, 0);
    ctx.lineTo(width1 - radius, 0);
    ctx.arc(width1 - radius, radius, radius, 1.5*Math.PI, 0.5*Math.PI, false);
    ctx.moveTo(width1 - radius, height);
    ctx.lineTo(radius, height);
    ctx.lineTo(radius, 0);
    ctx.fillStyle = "gray";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.font = '12px malgun gothic'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = "black";
    ctx.fillText(first + "일", width1 + 10, radius);
    ctx.closePath();

    // second bar
    ctx.beginPath();
    ctx.arc(radius, 55 + radius, radius, 0.5*Math.PI, 1.5*Math.PI, false);
    ctx.moveTo(radius, 55);
    ctx.lineTo(width2 - radius, 55);
    ctx.arc(width2 - radius, 55 + radius, radius, 1.5*Math.PI, 0.5*Math.PI, false);
    ctx.moveTo(width2 - radius, 55 + height);
    ctx.lineTo(radius, 55 + height);
    ctx.lineTo(radius, 55);
    ctx.fillStyle = "gray";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.font = '12px malgun gothic'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = "black";
    ctx.fillText(second + "일", width2 + 10, 55+radius);
    ctx.closePath();

    // third bar
    ctx.beginPath();
    ctx.arc(radius, 110 + radius, radius, 0.5*Math.PI, 1.5*Math.PI, false);
    ctx.moveTo(radius, 110);
    ctx.lineTo(width3 - radius, 110);
    ctx.arc(width3 - radius, 110 + radius, radius, 1.5*Math.PI, 0.5*Math.PI, false);
    ctx.moveTo(width3 - radius, 110 + height);
    ctx.lineTo(radius, 110 + height);
    ctx.lineTo(radius, 110);
    ctx.fillStyle = "gray";
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    ctx.font = '12px malgun gothic'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = "black";
    ctx.fillText(third + "일", width3 + 10, 110+radius);
    ctx.closePath();

    // fourth bar
    if (width4 > 0) {
        ctx.beginPath();
        ctx.arc(radius, 165 + radius, radius, 0.5*Math.PI, 1.5*Math.PI, false);
        ctx.moveTo(radius, 165);
        ctx.lineTo(width4 - radius, 165);
        ctx.arc(width4 - radius, 165 + radius, radius, 1.5*Math.PI, 0.5*Math.PI, false);
        ctx.moveTo(width4 - radius, 165 + height);
        ctx.lineTo(radius, 165 + height);
        ctx.lineTo(radius, 165);
        ctx.fillStyle = "gray";
        ctx.fill();
        ctx.closePath();

        ctx.beginPath();
        ctx.font = '12px malgun gothic'
        ctx.textBaseline = 'middle'
        ctx.fillStyle = "black";
        ctx.fillText(others + "일", width4 + 10, 165+radius);
        ctx.closePath();
    }
    else {
        ctx.beginPath();
        ctx.fillStyle = "gray";
        ctx.fillRect(0, 165, 5, 165 + height);
        ctx.closePath();

        ctx.beginPath();
        ctx.font = '12px malgun gothic'
        ctx.textBaseline = 'middle'
        ctx.fillStyle = "black";
        ctx.fillText(others + "일", 15, 165+radius);
        ctx.closePath();
    }    

    
}
