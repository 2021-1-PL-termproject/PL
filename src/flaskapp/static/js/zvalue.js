
google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawMultSeries1);
google.charts.setOnLoadCallback(drawMultSeries2);
google.charts.setOnLoadCallback(drawMultSeries3);

function drawMultSeries1() {
      var data = google.visualization.arrayToDataTable([
        ['활동성', '감지 횟수'],
        ['부동', A],
        ['미동', B],
        ['활동', C],
        ['매우 활동', D],
      ]);

      var options = {
        height: 300,
        width : 500,
        title: '활동성 그래프',
        chartArea: {width: '100%' },
        hAxis: {
          title: '활동성',
          minValue: 0
        },
        vAxis: {
          title: ''
        }
      };

      var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }



function drawMultSeries2() {
      var data = google.visualization.arrayToDataTable([
        ['', '운동 횟수', {role: 'style'}],
        ['실내운동', AA, 'green'],
        ['실외운동', BB, 'green'],
        ['하루평균 운동 횟수', CC, 'green'],
      ]);

      var options = {
        height: 300,
        width : 500,
        title: '운동 그래프',
        chartArea: {width: '100%' },
        hAxis: {
          title: '운동',
          minValue: 0
        },
        vAxis: {
          title: ''
        }
      };

      var chart = new google.visualization.BarChart(document.getElementById('chart_exer'));
      chart.draw(data, options);
    }

function drawMultSeries3() {
      var data = google.visualization.arrayToDataTable([
        ['', '외출', {role: 'style'}],
        ['외출', AAA, 'purple'],
        ['하루평균 외출 횟수', BBB, 'purple'],
      ]);

      var options = {
        height: 300,
        width : 500,
        title: '외출 그래프',
        chartArea: {width: '100%' },
        hAxis: {
          title: '외출',
          minValue: 0
        },
        vAxis: {
          title: ''
        }
      };

      var chart = new google.visualization.BarChart(document.getElementById('chart_out'));
      chart.draw(data, options);
    }