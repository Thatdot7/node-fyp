var update_realtime;

$(document).ready(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
	$(".power-level").show();
	real_time_chart();

	$("input[name='chartSelect']").on('change', function(){
		console.log($(this).val());
		if ($(this).val() == "real_time"){
			real_time_chart();
			$(".power-level").show();
		} else if ($(this).val() == "hourly"){
			clearInterval(update_realtime);
			column_chart("last_hours");
			$(".power-level").hide();
		} else {
			clearInterval(update_realtime);
			column_chart("last_days");
			$(".power-level").hide();
		}
	});
});    

function real_time_chart() {
	$.post('monitor', {"data" : "realtime_initial"}).done(function(posted_data){
		$('#graph').highcharts({
			chart: {
				type: 'spline',
				animation: Highcharts.svg, // don't animate in old IE
				marginRight: 10,
				events: {
					load: function() {
		    
						// set up the updating of the chart each second
						var series = this.series[0];
						update_realtime = setInterval(function() {
							$.post('monitor', {"data" : "realtime_initial"}).done(function(data){
								var x = (new Date()).getTime(), // current time
								y = parseFloat(data);
								$(".power").text(y);
								series.addPoint([x, y], true, true);
							});
						}, 1000);
					}
				}
			},
			title: {
				text: 'Real-time Power Consumption'
			},
			xAxis: {
				type: 'datetime',
				tickPixelInterval: 150
			},
			yAxis: {
				title: {
					text: 'Power (W)'
				},
				min: 0,
				max: 2400
			},
			tooltip: {
				formatter: function() {
					return Highcharts.dateFormat('%H:%M:%S of %d/%m/%Y', this.x) +'<br/>'+
					Highcharts.numberFormat(this.y, 2) + 'W';
				}
			},
			legend: {
				enabled: false
			},
			exporting: {
				enabled: false
			},
			credits: {
				enabled: false
			},
			series: [{
				name: 'Real Power',
				data: (function() {
					// generate an array of random data
					var data = [],
					time = (new Date()).getTime(),
					i;
					for (i = -19; i <= 0; i++) {
						data.push({
							x: time + i * 1000,
							y: parseFloat(posted_data)
						});
					}
					console.log(data);
					return data;
				})()
			}]
		});
	});
}


function column_chart(type) {

	var dateFormat;
	if(type == 'last_hours'){
		dateFormat = {hour: '%H:%M'};
	} else {
		dateFormat = {day: '%e. %b'};
	} 
		

	$.post('monitor', {"data" : type}).done(function(data){
		posted_data = JSON.parse(data);
	
		$('#graph').highcharts({
			chart: {
				type: 'column',
			},
			title: {
				text: 'Energy usage in the Last 24 hours'
			},
			xAxis: {
				type: 'datetime',
				dateTimeLabelFormat: dateFormat
			},
			yAxis: {
				min: 0,
				title: {
					text: 'Energy (kWh)'
				}
			},
			legend: {
				enabled: false
			},
			credits: {
				enabled: false
			},
			tooltip: {
				pointFormat: '{point.y:.4f}kWh',
			},
			series: [{
				data: posted_data.data
				
	            }]
        	});
	});
}
