import 'chart.js/auto'
import { Bar } from "react-chartjs-2";

export const StackedBarChart = ({ chartData, text }) => {
    return (
        <div>
            <Bar
                data={chartData}
                options={{
                    plugins: {
                        title: {
                            display: true,
                            font: {
                                size: 28
                            },
                            text: text
                        },
                        legend: {
                            display: false,
                        }
                    },
                    scales: {
                        x: {
                            stacked: true,
                        },
                        y: {
                            stacked: true,
                        }
                    }
                }}
            />
        </div>
    )
}