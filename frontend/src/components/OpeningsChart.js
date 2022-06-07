import { useEffect, useState } from "react";
import { DoughnutChart } from "./ChartDoughnut";
import LoadingSpinner from "./LoadingSpinner";

function OpeningsChart({ eco, url }) {

    useEffect(() => {
        const fetchPercentages = async () => {
            const res = await fetch(url).catch(err => {alert("An error has occured, please go back and try again")})
            const data = await res.json()
            setData({ data: data })
        }
        fetchPercentages()
    }, [])

    const [data, setData] = useState({})
    let flag = false;

    if (Object.keys(data).length !== 0) {

        let generalChartData = {
            labels: ['White Wins', 'Black Wins', 'Draws'],
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

        let variationsChartsData = []
        let variationNames = []
        let variationEngineEvals = []
        for (const variation in data["data"]["variations"]) {
            if (data["data"]["variations"][variation]["white_wins"] + data["data"]["variations"][variation]["black_wins"] + data["data"]["variations"][variation]["draws"] !== 0) {
                variationEngineEvals.push(data["data"]["variations"][variation]["engine_evaluation"])
                variationNames.push(variation)
                variationsChartsData.push({
                    labels: ['White Wins', 'Black Wins', 'Draws'],
                    datasets: [{
                        label: 'wdl',
                        data: [data["data"]["variations"][variation]["white_wins"], data["data"]["variations"][variation]["black_wins"], data["data"]["variations"][variation]["draws"]],
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 205, 86)'
                        ],
                        hoverOffset: 4
                    }]
                })
            }
        }

        const doughnutStyle = {
            margin: "auto",
            paddingBottom: "7%",
            width: "40%",
            height: "40%"
        }

        return (
            <div>
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={generalChartData} text={eco + " Side Advantage"} displayLabels={flag} />
                </div>
                <div>
                    <h1 style={{fontSize: "700%"}}>Variations</h1>
                </div>
                {variationsChartsData.map(function(variationsChartData, i){
                    return (
                        <div key={variationNames[i]} style={doughnutStyle}>
                            <DoughnutChart chartData={variationsChartData} text={variationNames[i]} displayLabels={flag} />
                            <p>Engine Evaluation: {variationEngineEvals[i]}</p>
                        </div>
                    )
                })}
            </div>
        )
    } else {
        return (
            <LoadingSpinner />
        )
    }
}

export default OpeningsChart;