import { useEffect, useState } from "react";
import { DoughnutChart } from "./Chart";

function OpeningsChart({ eco, url }) {

    useEffect(() => {
        const fetchPercentages = async () => {
            const res = await fetch(url)
            const data = await res.json()
            setData({ data: data })
        }
        fetchPercentages()
    }, [])

    const [data, setData] = useState({})

    if (Object.keys(data).length !== 0) {
        
        let generalChartData = {
            labels: ['White Wins', 'BLack Wins', 'Draws'],
            datasets: [{
            label: 'wdl',
            data: [data["data"][eco]["white_wins"], data["data"][eco]["black_wins"], data["data"][eco]["draws"]],
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
            }]
        }

        const doughnutStyle = {
            margin: "auto",
            paddingBottom: "7%",
            width: "40%",
            height: "40%"
        }

        return (
            <div style={doughnutStyle}>
                <DoughnutChart chartData={generalChartData} text={eco + " Side Advantage"} />
            </div>
        )
    }
}

export default OpeningsChart;