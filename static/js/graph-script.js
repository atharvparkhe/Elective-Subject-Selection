// SIDEBAR TOGGLE
var sidebarOpen = false;
var subjects_list = []
var sidebar = document.getElementById("sidebar");

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add("sidebar-responsive");
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove("sidebar-responsive");
    sidebarOpen = false;
  }
}

// Function to fetch data using Axios
function api_data() {
  return axios.get('http://127.0.0.1:8000/api/graph-data/')
    .then(response => response.data)
    .catch(error => {
      console.error('Error fetching chart data:', error);
      return [];
    });
}

// Function to update the bar chart data and render the chart
function updateBarChartWithData(barChart, newData) {

  barChart.updateOptions({
    series: [{
      data: newData.enrollments
    }],
    
    xaxis: {
      categories: newData.subjects
    }

  });
}

// Function to initialize the bar chart
function initializeBarChart() {

  var barChartOptions = {
    series: [{
      // data: [10, 8, 7]
      data: []
    }],
    chart: {
      type: 'bar',
      height: 350,
      toolbar: {
        show: false
      },
    },
    plotOptions: {
      bar: {
        distributed: true,
        borderRadius: 4,
        horizontal: false,
        columnWidth: '40%',
      }
    },
    dataLabels: {
      enabled: false
    },
    legend: {
      show: false
    },
    xaxis: {
      // categories: ["IOT",  "WT"],
      categories: []
    },
    yaxis: {
      title: {
        text: "Number of Students"
      }
    }
  };

  var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
  barChart.render();

  // Fetch data and update the bar chart when the page loads
  api_data().then(data => {
    updateBarChartWithData(barChart, data);
  });

}

initializeBarChart();

// Function to update the area chart data and render the chart
function updateAreaChartWithData(areaChart, newData) {
  areaChart.updateSeries([
    { name: 'Student Subject Enrollment', data: newData.enrollments },
    { name: 'Change requested FROM subject', data: newData.change_from },
    { name: 'Change requested TO subject', data: newData.change_to },
  ]);

  areaChart.updateOptions({
      labels: newData.subjects
  });
}

// Function to initialize the area chart
function initializeAreaChart() {
  var areaChartOptions = {
    series: [{
      name: 'Change requested FROM subject',
      data: []
    }, {
      name: 'Student Subject Enrollment',
      data: []
    },{
      name: 'Change requested TO subject',
      data: []
    }],
    chart: {
      height: 350,
      type: 'area',
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth'
    },
    labels: [],
    markers: {
      size: 0
    },
    yaxis: [
      {
        title: {
          text: 'Number of Students',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
    }
  };

  var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
  areaChart.render();

  // Fetch data and update the area chart when the page loads
  api_data().then(data => {
    updateAreaChartWithData(areaChart, data);
  });

}

initializeAreaChart();


//3RD CHART

function updatePieChartWithData(pieChart, newData) {
  pieChart.updateOptions({
      series: newData.dept_stu,
      labels: newData.depatments,
  });
}

var piechartoptions = {
  // series: [70, 55, 13, 43, 22],
  series: [],

  // labels: ['IT', 'COMP', 'ETC', 'MECH', 'CIVIL'],
  labels: [],

  //for displaying no. of students instead of percentage
  dataLabels: {
    formatter: function (val, opts) {
        return opts.w.config.series[opts.seriesIndex]
    },
  },
  
  chart: {
  width: 380,
  type: 'donut',
},

legend: {
    position: 'bottom'
  },

  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]

};

var piechart = new ApexCharts(document.querySelector("#pie-chart"), piechartoptions);
piechart.render();
api_data().then(data => {
<<<<<<< HEAD
// console.log(data.dept_stu);
=======
  // console.log(data.dept_stu);
>>>>>>> 90bef8dbff5877e1fff810da2cc3765f5fb44ff7
// console.log(data.depatments);
  updatePieChartWithData(piechart, data);
});


//4TH CHART

function updateRadarChartWithData(pieChart, newData) {
  pieChart.updateOptions({
      series: newData.radar,
      xaxis: {
        categories: newData.subjects
      }
  });
}

var radarchartoptions = {
  // series: [
    // {
    //   name: 'IT',
    //   data: [80, 50, 30],
    // }, {
    //   name: 'COMP',
    //   data: [20, 30, 40],
    // }, {
    //   name: 'ETC',
    //   data: [44, 76, 78],
    // }
// ],
  series: [],
  chart: {
  height: 350,
  type: 'radar',
  dropShadow: {
    enabled: true,
    blur: 1,
    left: 1,
    top: 1
  }
},
stroke: {
  width: 2
},
fill: {
  opacity: 0.1
},
markers: {
  size: 0
},
xaxis: {
  categories: []
}
};

var radarchart = new ApexCharts(document.querySelector("#radar-chart"), radarchartoptions);
radarchart.render();

api_data().then(data => {
  console.warn(data.radar)
  updateRadarChartWithData(radarchart, data);
});


// SIDEBAR TOGGLE
// var sidebarOpen = false;
// var sidebar = document.getElementById("sidebar");

// function openSidebar() {
//   if (!sidebarOpen) {
//     sidebar.classList.add("sidebar-responsive");
//     sidebarOpen = true;
//   }
// }

// function closeSidebar() {
//   if (sidebarOpen) {
//     sidebar.classList.remove("sidebar-responsive");
//     sidebarOpen = false;
//   }
// }

// // Function to fetch data using Axios
// function fetchData() {
//   return axios.get('http://127.0.0.1:8000/api/graph-data/')  // Replace '/api/chart-data/' with your actual API endpoint URL
//     .then(response => response.data)
//     .catch(error => {
//       console.error('Error fetching chart data:', error);
//       return [];
//     });
// }

// // Function to update the bar chart data and render the chart
// function updateBarChartWithData(barChart, newData) {
//   barChart.updateOptions({
//     series: [{
//       data: newData
//     }]
//   });
// }

// // Function to initialize the bar chart
// function initializeBarChart() {
//   var barChartOptions = {
//     series: [{
//       data: [10, 8, 6, 8]
//     }],
//     chart: {
//       type: 'bar',
//       height: 350,
//       toolbar: {
//         show: false
//       },
//     },
//     colors: [
//       "#246dec",
//       "#cc3c43",
//       "#367952",
//       "#f5b74f",
//       "#4f35a1"
//     ],
//     plotOptions: {
//       bar: {
//         distributed: true,
//         borderRadius: 4,
//         horizontal: false,
//         columnWidth: '40%',
//       }
//     },
//     dataLabels: {
//       enabled: false
//     },
//     legend: {
//       show: false
//     },
//     xaxis: {
//       categories: ["IOT", "CFCS", "SOFT COMP", "WT"],
//     },
//     yaxis: {
//       title: {
//         text: "No of Students"
//       }
//     }
//   };

//   var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
//   barChart.render();

//   // Fetch data and update the bar chart when the page loads
//   fetchData().then(data => {
//     updateBarChartWithData(barChart, data);
//   });

//   // Fetch data and update the bar chart periodically (example: every 5 seconds)
//   setInterval(() => {
//     fetchData().then(data => {
//       updateBarChartWithData(barChart, data);
//     });
//   }, 5000);
// }

// initializeBarChart();

// // Function to update the area chart data and render the chart
// function updateAreaChartWithData(areaChart, newData) {
//   areaChart.updateSeries([
//     { name: 'student opted for subjects', data: newData.opted },
//     { name: 'student changed subject', data: newData.changed }
//   ]);
// }

// // Function to initialize the area chart
// function initializeAreaChart() {
//   var areaChartOptions = {
//     series: [{
//       name: 'student opted for subjects',
//       data: [10, 8, 6, 8]
//     }, {
//       name: 'student changed subject',
//       data: [5, 12, 4, 8]
//     }],
//     chart: {
//       height: 350,
//       type: 'area',
//       toolbar: {
//         show: false,
//       },
//     },
//     colors: ["#367952", "#cc3c43"],
//     dataLabels: {
//       enabled: false,
//     },
//     stroke: {
//       curve: 'smooth'
//     },
//     labels: ["IOT", "CFCS", "SOFT COMP", "WT"],
//     markers: {
//       size: 0
//     },
//     yaxis: [
//       {
//         title: {
//           text: 'student opted for subject',
//         },
//       },
//       {
//         opposite: true,
//         title: {
//           text: 'student changed subject',
//         },
//       },
//     ],
//     tooltip: {
//       shared: true,
//       intersect: false,
//     }
//   };

//   var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
//   areaChart.render();

//   // Fetch data and update the area chart when the page loads
//   fetchData().then(data => {
//     updateAreaChartWithData(areaChart, data);
//   });

//   // Fetch data and update the area chart periodically (example: every 5 seconds)
//   setInterval(() => {
//     fetchData().then(data => {
//       updateAreaChartWithData(areaChart, data);
//     });
//   }, 5000);
// }

// initializeAreaChart();
