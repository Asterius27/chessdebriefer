import 'chart.js/auto'
import { Doughnut } from "react-chartjs-2";

export const DoughnutChart = ({ chartData, text }) => {
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
                        }
                    }
                }}
            />
        </div>
    )
}