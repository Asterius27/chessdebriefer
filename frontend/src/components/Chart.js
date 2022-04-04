import 'chart.js/auto'
import { Doughnut } from "react-chartjs-2";

export const DoughnutChart = ({ chartData }) => {
    return (
        <div>
            <Doughnut
                data={chartData}
                options={{
                    plugins: {
                        title: {
                            display: true,
                            text: "Your wdl stats"
                        },
                        legend: {
                            display: true,
                            position: "bottom"
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