var canvas = document.getElementById("canvasreport");
var ctx = canvas.getContext("2d");
var radius = canvas.height / 2;
ctx.translate(radius, radius);
radius = radius * 0.9;
drawClock();

function drawClock() {
  drawFace(ctx, radius);
  drawNumbers(ctx, radius);
  drawTime(ctx, radius);
}

function drawFace(ctx, radius) {
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, 2 * Math.PI);
  ctx.fillStyle = "#f3f3f3";
  ctx.strokeStyle = "black";
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.strokeStyle = "rgba(250, 250, 2, 0.03)";
  ctx.lineWidth = radius * 0.02;
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(0, 0, radius * 0.05, 0, 2 * Math.PI);
  ctx.fillStyle = "black";
  ctx.fill();
}

function drawNumbers(ctx, radius) {
  var ang;
  var num;
  ctx.font = radius * 0.12 + "px arial";
  ctx.textBaseline = "middle";
  ctx.textAlign = "center";
  for (num = 0; num < 24; num++) {
    ang = (num * Math.PI) / 12;
    ctx.rotate(ang);
    ctx.translate(0, -radius * 0.8);
    ctx.rotate(-ang);
    ctx.fillText(num.toString(), 0, 0);
    ctx.rotate(ang);
    ctx.translate(0, radius * 0.8);
    ctx.rotate(-ang);
  }
}

function getsleepHr() {
  return sleep_hr;
}
function getsleepMin() {
  return sleep_min;
}
function getsleepSec() {
  return sleep_sec;
}

function getawakeHr() {
  return awake_hr;
}
function getawakeMin() {
  return awake_min;
}
function getawakeSec() {
  return awake_sec;
}

function getbreakfastHr() {
  return breakfast_hr;
}
function getbreakfastMin() {
  return breakfast_min;
}
function getbreakfastSec() {
  return breakfast_sec;
}

function getlunchHr() {
  return lunch_hr;
}
function getlunchMin() {
  return lunch_min;
}
function getlunchSec() {
  return lunch_sec;
}

function getdinnerHr() {
  return dinner_hr;
}
function getdinnerMin() {
  return dinner_min;
}
function getdinnerSec() {
  return dinner_sec;
}

function drawTime(ctx, radius) {
  var sleep_hr = getsleepHr();
  var sleep_min = getsleepMin();
  var sleep_sec = getsleepSec();
  var sleep;
  var awake_hr = getawakeHr();
  var awake_min = getawakeMin();
  var awake_sec = getawakeSec();
  var awake;
  var breakfast_hr= getbreakfastHr()
  var breakfast_min = getbreakfastMin();
  var breakfast_sec = getbreakfastSec();
  var breakfast;
  var lunch_hr = getlunchHr();
  var lunch_min = getlunchMin();
  var lunch_sec = getlunchSec();
  var lunch;
  var dinner_hr = getdinnerHr();
  var dinner_min = getdinnerMin();
  var dinner_sec = getdinnerSec();
  var dinner;
  sleep =
    (sleep_hr * Math.PI) / 12 +
    (sleep_min * Math.PI) / (12 * 60) +
    (sleep_sec * Math.PI) / (12 * 3600);
  awake =
    (awake_hr * Math.PI) / 12 +
    (awake_min * Math.PI) / (12 * 60) +
    (awake_sec * Math.PI) / (12 * 3600);
  if (typeof sleep !== "undefined") {
    if (typeof awake !== "undefined") {
      if (sleep > awake) {
        for (num = sleep; num < 2 * Math.PI; num += 0.01) {
          drawHand(ctx, num, radius * 0.96, radius * 0.1);
        }
        for (num = 0; num < awake; num += 0.01) {
          drawHand(ctx, num, radius * 0.96, radius * 0.1);
        }
      } else {
        for (num = sleep; num < awake; num += 0.01) {
          drawHand(ctx, num, radius * 0.96, radius * 0.1);
        }
      }
    }
  }

  if (typeof breakfast_hr != "undefined") {
    breakfast =
      (breakfast_hr * Math.PI) / 12 +
      (breakfast_min * Math.PI) / (12 * 60) +
      (breakfast_sec * Math.PI) / (12 * 3600);
    for (i = 1; i < 20; i++) {
      drawHand(ctx, breakfast, radius * 0.95, radius * 0.1);
    }
  }

  if (typeof lunch_hr != "undefined") {
    lunch =
      (lunch_hr * Math.PI) / 12 +
      (lunch_min * Math.PI) / (12 * 60) +
      (lunch_sec * Math.PI) / (12 * 3600);
    for (i = 1; i < 20; i++) {
      drawHand(ctx, lunch, radius * 0.95, radius * 0.1);
    }
  }

  if (typeof dinner_hr != "undefined") {
    dinner =
      (dinner_hr * Math.PI) / 12 +
      (dinner_min * Math.PI) / (12 * 60) +
      (dinner_sec * Math.PI) / (12 * 3600);
    for (i = 1; i < 20; i++) {
      drawHand(ctx, dinner, radius * 0.95, radius * 0.1);
    }
  }
}

function drawHand(ctx, pos, length, width) {
  ctx.beginPath();
  ctx.lineWidth = width;
  ctx.lineCap = "round";
  ctx.moveTo(0, 0);
  ctx.rotate(pos);
  ctx.lineTo(0, -length);
  ctx.stroke();
  ctx.rotate(-pos);
}
