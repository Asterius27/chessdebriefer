import 'chart.js/auto'
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { Chart } from 'chart.js';
import { Doughnut } from "react-chartjs-2";
Chart.register(ChartDataLabels);

export const DoughnutChart = ({ chartData, text, displayLabels }) => {
    return (
        <div className='div2PDF'>
            <Doughnut
                data={chartData}
                options={{
                    plugins: {
                        title: {
                            display: true,
                            font: {
                                size: "30%"
                            },
                            text: text
                        },
                        legend: {
                            display: true,
                            position: "bottom",
                            labels: {
                                font: {
                                    size: "15%"
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let percentage = 0.
                                    if (context.dataset.data[0] + context.dataset.data[1] + context.dataset.data[2] !== 0)
                                    {
                                        percentage = ((context.parsed * 1.) / (context.dataset.data[0] + context.dataset.data[1] + context.dataset.data[2])) * 100.
                                    }
                                    return context.label + ": " + context.formattedValue + " (" + percentage.toFixed(2) + " %)"
                                }
                            }
                        },
                        datalabels: {
                            display: displayLabels,
                            font: {
                                weight: "bold",
                                size: "25%"
                            },
                            color: "white"
                        }
                    }
                }}
            />
        </div>
    )
}