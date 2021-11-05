
google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawMultSeries);

function drawMultSeries() {
      var data = google.visualization.arrayToDataTable([
        ['활동성', '감지 횟수'],
        ['부동', A],
        ['미동', B],
        ['활동', C],
        ['매우 활동', D],
      ]);

      var options = {
        height: 300,
        width : 300,
        title: '활동량 점수',
        chartArea: {width: '100%' },
        hAxis: {
          title: '',
          minValue: 0
        },
        vAxis: {
          title: ''
        }
      };

      var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }