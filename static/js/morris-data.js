$(function() {
	
    Morris.Line({
        element: 'morris-area-chart',
        data: [{
            week: 0,
            currentRate: 300,
            ideal: 300,
        }, {
            week: 1,
            currentRate: 280,
            ideal: 270,
        }, {
        	week: 2,
        	currentRate: 260,
            ideal: 240,
        }, {
        	week: 3,
        	currentRate: 240,
            ideal: 210,
        }, {
        	week: 4,
        	currentRate: 220,
            ideal: 180,
        }, {
        	week: 5,
        	currentRate: 200,
            ideal: 150,
        }, {
            week: 6,
            currentRate: 180,
            ideal: 120,
        }, {
            week: 7,
            currentRate: 160,
            ideal: 90,
        }, {
            week: 8,
            currentRate: 140,
            ideal: 60,
        }, {
            week: 9,
            currentRate: 120,
            ideal: 30, 
        }, {
        	week: 10,
        	currentRate: 100,
        	ideal: 0,
        }],
        xkey: "week",
        ykeys: ['currentRate','ideal'],
        labels: ['currentRate','ideal'],
        pointSize: 2,
        hideHover: 'auto',
        hoverCallback: function (index, options, content, row) { 
        	var pos = content.search("<div class='morris-hover-point'");
        	var res = content.slice(pos, content.length);
        	return "Week " + index + "<p>" + res;
        },
        resize: true,
        behaveLikeLine: true,
        xLabelFormat: function (x) {return ""},
    });
    
    Morris.Line({
        element: 'morris-area-chart1',
        data: [{
        	week: 0,
        	schillers: 2.5,
        }, {
            week: 1,
            schillers: 22.5,
        }, {
            week: 2,
            schillers: 20,
        }, {
        	week: 3,
            schillers: 15,
        }, {
        	week: 4,
            schillers: 15,
        }, {
        	week: 5,
            schillers: 10,
        }, {
        	week: 6,
            schillers: 10,
        }, {
            week: 7,
            schillers: 5,
        }, {
            week: 8,
            schillers: 5,
        }, {
            week: 9,
            schillers: 25,
        }, {
            week: 10,
            schillers: 20  
        }],
        
        xkey: "week",
        ykeys: ['schillers'],
        labels: ['schillers'],
        pointSize: 2,
        hideHover: 'auto',
        hoverCallback: function (index, options, content, row) { 
        	var pos = content.search("<div class='morris-hover-point'");
        	var res = content.slice(pos, content.length);
        	return "Week " + index + "<p>" + res;
        },
        resize: true,
        smooth: false,
        behaveLikeLine: true,
        xLabelFormat: function (x) {return ""},
    });

    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            y: '2006',
            a: 100,
            b: 90
        }, {
            y: '2007',
            a: 75,
            b: 65
        }, {
            y: '2008',
            a: 50,
            b: 40
        }, {
            y: '2009',
            a: 75,
            b: 65
        }, {
            y: '2010',
            a: 50,
            b: 40
        }, {
            y: '2011',
            a: 75,
            b: 65
        }, {
            y: '2012',
            a: 100,
            b: 90
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        hideHover: 'auto',
        resize: true
    });

});
