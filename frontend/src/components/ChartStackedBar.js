import 'chart.js/auto'
import { Bar } from "react-chartjs-2";

export const StackedBarChart = ({ chartData, text }) => {
    return (
        <div className='div2PDF'>
            <Bar
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
                            display: true
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