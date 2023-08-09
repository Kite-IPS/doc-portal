 // Placeholder data for the doughnut graph
 var ctx = document.getElementById('myDoughnutChart').getContext('2d');
 var myDoughnutChart = new Chart(ctx, {
   type: 'doughnut',
   data: {
     labels: ['Total', 'Submitted', 'Pending'],
     datasets: [{
       data: [1200, 800, 150],
       backgroundColor: ['#FF6B6B', '#6EE7B7', '#FFC107']
     }]
   },
   options: {
     responsive: true,
     maintainAspectRatio: false,
     cutout: 60, // Adjust the cutout value for thinner doughnut
     plugins: {
       legend: {
         display: true,
         position: 'right',
         labels: {
           font: {
             size: 14,
           }
         }
       },
       tooltip: {
         enabled: false,
       },
     },
     onHover: function(event, elements) {
       var tooltip = document.getElementById('tooltip');
       if (elements && elements.length > 0) {
         var index = elements[0].index;
         var value = myDoughnutChart.data.datasets[0].data[index];
         var label = myDoughnutChart.data.labels[index];
         tooltip.innerHTML = `<strong>${label}</strong><br>${value} documents`;
         tooltip.style.left = event.clientX + 'px';
         tooltip.style.top = event.clientY + 'px'; // Adjust tooltip position
         tooltip.style.opacity = '1';
       } else {
         tooltip.style.opacity = '0';
       }
     },
   },
 });