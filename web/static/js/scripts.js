const ctx1 = document.getElementById('chart1').getContext('2d');
const percent_value = 554;
const chart = new Chart(ctx1, {
    type: 'doughnut',
    data: {
        labels: ['CO',],
        datasets: [{
            label: 'CO',
            data: [percent_value, 1500 - percent_value],
            backgroundColor: ['#00baa6', '#ededed']
        }]
    },
    options: {

    }
});

const ctx2 = document.getElementById('chart2').getContext('2d');
const percent_value2 = 40;
const chart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['PM2.5',],
        datasets: [{
            label: 'PM2.5',
            data: [percent_value, 200 - percent_value],
            backgroundColor: ['#f01e2c', '#ededed']
        }]
    },
    options: {}
});

const ctx3 = document.getElementById('chart3').getContext('2d');
const percent_value3 = 29;
const chart3 = new Chart(ctx3, {
    type: 'doughnut',
    data: {
        labels: ['Temperature',],
        datasets: [{
            label: 'Temperature',
            data: [percent_value, 100 - percent_value],
            backgroundColor: ['#00baa6', '#ededed']
        }]
    },
    options: {

    }
});

const ctx4 = document.getElementById('chart4').getContext('2d');
const percent_value4 = 40;
const chart4 = new Chart(ctx4, {
    type: 'doughnut',
    data: {
        labels: ['Humidity',],
        datasets: [{
            label: 'Humidity',
            data: [percent_value, 200 - percent_value],
            backgroundColor: ['#f01e2c', '#ededed']
        }]
    },
    options: {}
});

const ctx5 = document.getElementById("chart5").getContext('2d');
const chart5 = new Chart(ctx5, {
    type: 'line',
    data: {
        labels: ["Sunday", "Monday", "Tuesday",
            "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday",
            "Wednesday", "Thursday", "Friday", "Saturday"],
        datasets: [{
            label: 'Temperature',
            backgroundColor: 'rgba(161, 198, 247, 1)',
            borderColor: 'rgb(47, 128, 237)',
            data: [500, 400, 600, 900, 300, 600, 500, 500, 400, 600, 900, 300, 600, 500],
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }

        }
    },
});

const ctx6 = document.getElementById("chart6").getContext('2d');
const chart6 = new Chart(ctx6, {
    type: 'line',
    data: {
        labels: ["Sunday", "Monday", "Tuesday",
            "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday",
            "Wednesday", "Thursday", "Friday", "Saturday"],
        datasets: [{
            label: 'PPM',
            backgroundColor: 'rgba(161, 198, 247, 1)',
            borderColor: 'rgb(47, 128, 237)',
            data: [500, 400, 600, 900, 300, 600, 500, 500, 400, 600, 900, 300, 600, 500],
        },
        {
            label: 'CO',
            backgroundColor: 'rgba(161, 128, 47, 1)',
            borderColor: 'rgb(47, 128, 237)',
            data: [40, 60, 30, 90, 30, 70, 50, 50, 40, 80, 20, 30, 30, 20],
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }

        }
    },
});

