import 'chart.js/auto'
import { Bar } from "react-chartjs-2";

export const BarChart = ({ chartData, text }) => {
    return (
        <div>
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
                            display: false,
                        }
                    }
                }}
            />
        </div>
    )
}