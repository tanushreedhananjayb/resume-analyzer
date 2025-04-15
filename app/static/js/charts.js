document.addEventListener("DOMContentLoaded", () => {
    const data = JSON.parse(document.getElementById("jobData").textContent);
    const ctx = document.getElementById("matchChart").getContext("2d");
  
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.titles,
        datasets: [{
          label: 'Match Score (%)',
          data: data.scores,
          backgroundColor: 'rgba(13, 110, 253, 0.7)',
          borderColor: 'rgba(13, 110, 253, 1)',
          borderWidth: 1,
          borderRadius: 5
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true, max: 100 }
        }
      }
    });
  });
  