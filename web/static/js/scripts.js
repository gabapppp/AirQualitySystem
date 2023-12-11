var chart = JSC.chart('chartTemp', {
    debug: true,
    title: {
        label_text: 'Temperature',
        position: 'center'
    },
    legend_visible: false,
    yAxis: [
        {
            line_width: 0,
            defaultTick_enabled: false,
            scale_range: [0, 50]
        }
    ],
    xAxis: [
        {
            defaultTick_gridLine_width: 'column',
            spacingPercentage: 0.15
        }
    ],
    defaultSeries: {
        type: 'gauge column roundCaps',
        shape: {
            innerSize: '70%',
            label: [
                {
                    text: '%value °C',
                    verticalAlign: 'middle',
                    style_fontSize: 20
                }
            ]
        }
    },
    series: [
        {
            pointValue: '{%value/80}',
            palette: {
                colors: ['#77e6b4']
            },
            points: [['value', 29]]
        }
    ]
});

var chart2 = JSC.chart('chartHum', {
    debug: true,
    title: {
        label_text: 'Humidity',
        position: 'center'
    },
    legend_visible: false,
    defaultTooltip_enabled: false,
    xAxis_spacingPercentage: 0.4,
    yAxis: [
        {
            line_width: 0,
            defaultTick_enabled: false,
            scale_range: [0, 100]
        },
        {
            id: 'ax2',
            scale_range: [0, 100],
            defaultTick: {
                padding: 10,
                enabled: false
            },
            customTicks: [0, 30, 60, 70, 80, 100],
            line: {
                width: 10,
                color: 'smartPalette:pal2'
            }
        }
    ],
    xAxis: [
        {
            defaultTick_gridLine_width: 'column',
            spacingPercentage: 0.15
        }
    ],
    defaultSeries: {
        type: 'gauge column roundCaps',
        shape: {
            innerSize: '70%',
            label: [
                {
                    text: '%value %',
                    verticalAlign: 'middle',
                    style_fontSize: 20
                }
            ]
        }
    },
    series: [
        {
            palette: {
                id: 'pal2',
                pointValue: '{%value/100}',
                colors: [
                    '#ffffd9',
                    '#edf8b0',
                    '#c7e9b4',
                    '#7fcdbb',
                    '#41b6c3',
                    '#1d91c0',
                    '#225ea8',
                    '#253494',
                    '#081d58',
                ],
            },
            points: [['value', 71]]
        }
    ]
});

var chart3 = JSC.chart('chartCO', {
    debug: true,
    title: {
        label_text: 'CO',
        position: 'center'
    },
    legend_visible: false,
    yAxis: [
        {
            line_width: 0,
            defaultTick_enabled: false,
            scale_range: [0, 300]
        }
    ],
    xAxis: [
        {
            defaultTick_gridLine_width: 'column',
            spacingPercentage: 0.15
        }
    ],
    defaultSeries: {
        type: 'gauge column roundCaps',
        shape: {
            innerSize: '70%',
            label: [
                {
                    text: '%value ppm',
                    verticalAlign: 'middle',
                    style_fontSize: 20
                }
            ]
        }
    },
    series: [
        {
            pointValue: '{%value/80}',
            palette: {
                colors: ['#77e6b4']
            },
            points: [['value', 68]]
        }
    ]
});

var chart4 = JSC.chart('chartCO2', {
    debug: true,
    title: {
        label_text: 'Pollution Gas (from MQ135)',
        position: 'center'
    },
    legend_visible: false,
    yAxis: [
        {
            line_width: 0,
            defaultTick_enabled: false,
            scale_range: [10, 1000]
        }
    ],
    xAxis: [
        {
            defaultTick_gridLine_width: 'column',
            spacingPercentage: 0.15
        }
    ],
    defaultSeries: {
        type: 'gauge column roundCaps',
        shape: {
            innerSize: '70%',
            label: [
                {
                    text: '%value ppm',
                    verticalAlign: 'middle',
                    style_fontSize: 20
                }
            ]
        }
    },
    series: [
        {
            pointValue: '{%value/80}',
            palette: {
                colors: ['#77e6b4']
            },
            points: [['value', 398]]
        }
    ]
});

var chart5 = JSC.chart('chartDust', {
    debug: true,
    title: {
        label_text: 'PM 2.5',
        position: 'center'
    },
    legend_visible: false,
    yAxis: [
        {
            line_width: 0,
            defaultTick_enabled: false,
            scale_range: [0, 50]
        }
    ],
    xAxis: [
        {
            defaultTick_gridLine_width: 'column',
            spacingPercentage: 0.15
        }
    ],
    defaultSeries: {
        type: 'gauge column roundCaps',
        shape: {
            innerSize: '70%',
            label: [
                {
                    text: '%value µg/m³',
                    verticalAlign: 'middle',
                    style_fontSize: 20
                }
            ]
        }
    },
    series: [
        {
            pointValue: '{%value/80}',
            palette: {
                colors: ['#77e6b4']
            },
            points: [['value', 29]]
        }
    ]
});

function getPoints(i) {
    var extraY = i * 20;
    var points = [
        { x: "1/1/2020", y: 65 },
        { x: "2/1/2020", y: 67 },
        { x: "3/1/2020", y: 72 },
        { x: "4/1/2020", y: 66 },
        { x: "5/1/2020", y: 84 },
        { x: "6/1/2020", y: 74 },
        { x: "7/1/2020", y: 72 },
        { x: "8/1/2020", y: 84 }
    ];
    return points.map(function (p) {
        return { x: p.x, y: p.y + extraY };
    });
};

var chart6 = JSC.chart('graphTempHum', {
    debug: true,
    type: 'line',
    legend_visible: false,
    xAxis: {
        crosshair_enabled: true,
        scale: { type: 'time' }
    },
    yAxis: {
        orientation: 'opposite',
        formatString: 'c'
    },
    defaultSeries: {
        firstPoint_label_text: '<b>%seriesName</b>',
        defaultPoint_marker: {
            type: 'circle',
            size: 8,
            fill: 'white',
            outline: { width: 2, color: 'currentColor' }
        }
    },
    title_label_text: 'Costs (Last 6 Months)',
    series: [
        {
            name: 'Temperature',
            points: [
                ['1/1/2020', 29.9],
                ['2/1/2020', 97.5],
                ['3/1/2020', 110.4],
                ['4/1/2020', 129.2],
                ['5/1/2020', 144.0],
                ['6/1/2020', 176.0]
            ]
        },
        {
            name: 'Humidity',
            points: [
                ['1/1/2020', 86.9],
                ['2/1/2020', 79.5],
                ['3/1/2020', 65.4],
                ['4/1/2020', 67.2],
                ['5/1/2020', 73.0],
                ['6/1/2020', 76.0]
            ]
        }
    ]
});

var chart7 = JSC.chart('graphDust', {
    debug: true,
    type: 'line',
    legend_visible: false,
    xAxis: {
        crosshair_enabled: true,
        scale: { type: 'time' }
    },
    yAxis: {
        orientation: 'opposite',
        formatString: 'c'
    },
    defaultSeries: {
        firstPoint_label_text: '<b>%seriesName</b>',
        defaultPoint_marker: {
            type: 'circle',
            size: 8,
            fill: 'white',
            outline: { width: 2, color: 'currentColor' }
        }
    },
    title_label_text: 'Costs (Last 6 Months)',
    series: [
        {
            name: 'CO',
            points: [
                ['1/1/2020', 200.9],
                ['2/1/2020', 130.5],
                ['3/1/2020', 100.4],
                ['4/1/2020', 120.2],
                ['5/1/2020', 140.0],
                ['6/1/2020', 160.0]
            ]
        },
        {
            name: 'Pollution Gas',
            points: [
                ['1/1/2020', 400.9],
                ['2/1/2020', 200.5],
                ['3/1/2020', 300.4],
                ['4/1/2020', 360.2],
                ['5/1/2020', 330.0],
                ['6/1/2020', 410.0]
            ]
        },
        {
            name: 'PM 2.5',
            points: [
                ['1/1/2020', 12.9],
                ['2/1/2020', 11.5],
                ['3/1/2020', 9.4],
                ['4/1/2020', 10.2],
                ['5/1/2020', 17.0],
                ['6/1/2020', 15.0]
            ]
        }
    ]
});