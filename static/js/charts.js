document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/summary')
        .then(res => res.json())
        .then(data => {

            // Pie Chart - Spending by Category
            const pieCtx = document.getElementById('pieChart');
            if (pieCtx && data.categories.length > 0) {
                new Chart(pieCtx, {
                    type: 'doughnut',
                    data: {
                        labels: data.categories,
                        datasets: [{
                            data: data.category_amounts,
                            backgroundColor: [
                                '#667eea', '#f093fb', '#4facfe',
                                '#43e97b', '#fa709a', '#fee140', '#a18cd1'
                            ],
                            borderWidth: 0,
                            hoverOffset: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 20,
                                    font: { family: 'Poppins', size: 12 }
                                }
                            },
                            title: {
                                display: true,
                                text: 'Spending by Category',
                                font: { family: 'Poppins', size: 16, weight: '600' },
                                color: '#333',
                                padding: { bottom: 20 }
                            }
                        }
                    }
                });
            }

            // Bar Chart - Spending by Month
            const barCtx = document.getElementById('barChart');
            if (barCtx && data.months.length > 0) {
                new Chart(barCtx, {
                    type: 'bar',
                    data: {
                        labels: data.months.reverse(),
                        datasets: [{
                            label: 'Amount Spent (₹)',
                            data: data.monthly_amounts.reverse(),
                            backgroundColor: 'rgba(102, 126, 234, 0.8)',
                            borderRadius: 8,
                            borderSkipped: false
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: false },
                            title: {
                                display: true,
                                text: 'Monthly Spending',
                                font: { family: 'Poppins', size: 16, weight: '600' },
                                color: '#333',
                                padding: { bottom: 20 }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: '#f0f0f0' },
                                ticks: {
                                    font: { family: 'Poppins' },
                                    callback: function(value) { return '₹' + value; }
                                }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { font: { family: 'Poppins' } }
                            }
                        }
                    }
                });
            }
        });
});