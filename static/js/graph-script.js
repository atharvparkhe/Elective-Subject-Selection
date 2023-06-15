// SIDEBAR TOGGLE

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
  if(!sidebarOpen) {
    sidebar.classList.add("sidebar-responsive");
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if(sidebarOpen) {
    sidebar.classList.remove("sidebar-responsive");
    sidebarOpen = false;
  }
}



// ---------- CHARTS ----------

// BAR CHART
var barChartOptions = {
  series: [{
    data: [10, 8, 6, 8]
  }],
  chart: {
    type: 'bar',
    height: 350,
    toolbar: {
      show: false
    },
  },
  colors: [
    "#246dec",
    "#cc3c43",
    "#367952",
    "#f5b74f",
    "#4f35a1"
  ],
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
    categories: ["IOT", "CFCS", "SOFT COMP", "WT"],
  },
  yaxis: {
    title: {
      text: "No of Students"
    }
  }
};

var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
barChart.render();

var areaChartOptions = {
  series: [{
    name: 'student opted for subjects',
    data: [10, 8, 6, 8]
  }, {
    name: 'student changed subject',
    data: [5, 12, 4, 8]
  }],
  chart: {
    height: 350,
    type: 'area',
    toolbar: {
      show: false,
    },
  },
  colors: ["#367952", "#cc3c43"],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth'
  },
  labels: ["IOT", "CFCS", "SOFT COMP", "WT"],
  markers: {
    size: 0
  },
  yaxis: [
    {
      title: {
        text: 'student opted for subject',
      },
    },
    {
      opposite: true,
      title: {
        text: 'student changed subject',
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