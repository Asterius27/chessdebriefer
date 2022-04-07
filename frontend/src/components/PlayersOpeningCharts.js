import { useEffect, useState } from "react";
import { DoughnutChart } from "./ChartDoughnut";

function GenerateCharts({ data, eco, name }) {

    const doughnutStyle = {
        margin: "auto",
        paddingBottom: "7%",
        width: "40%",
        height: "40%"
    }

    let generalChartData = {
        labels: ['Wins', 'Losses', 'Draws'],
        datasets: [{
            label: 'wdl',
            data: [data["data"][eco]["general stats"]["your wins"], data["data"][eco]["general stats"]["your losses"], data["data"][eco]["general stats"]["your draws"]],
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
        }]
    }

    let whiteChartData
    if (Object.keys(data["data"][eco]["side stats"]["white"]).length !== 0) {
        whiteChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"][eco]["side stats"]["white"]["white"]["your wins"], data["data"][eco]["side stats"]["white"]["white"]["your losses"], data["data"][eco]["side stats"]["white"]["white"]["your draws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    }

    let blackChartData
    if (Object.keys(data["data"][eco]["side stats"]["black"]).length !== 0) {
        blackChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"][eco]["side stats"]["black"]["black"]["your wins"], data["data"][eco]["side stats"]["black"]["black"]["your losses"], data["data"][eco]["side stats"]["black"]["black"]["your draws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    }

    let variationsChartsData = []
    let variationNames = []
    for (const variation in data["data"][eco]["variations stats"]) {
        variationNames.push(variation)
        variationsChartsData.push({
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"][eco]["variations stats"][variation]["your wins"], data["data"][eco]["variations stats"][variation]["your losses"], data["data"][eco]["variations stats"][variation]["your draws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        })
    }

    return (
        <div key={eco}>
            <div>
                <h1 style={{fontSize: "700%"}}>{eco}</h1>
            </div>
            <div style={doughnutStyle}>
                <DoughnutChart chartData={generalChartData} text={name + "'s " + eco + " wdl"} />
            </div>
            {whiteChartData ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={whiteChartData} text={name + "'s " + eco + " white wdl"} />
                </div> : <div></div>
            }
            {blackChartData ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={blackChartData} text={name + "'s " + eco + " black wdl"} />
                </div> : <div></div>
            }
            <div>
                <h1 style={{fontSize: "400%"}}>Variations</h1>
            </div>
            {variationsChartsData.map(function(variationsChartData, i){
                return (
                    <div key={variationNames[i]} style={doughnutStyle}>
                        <DoughnutChart chartData={variationsChartData} text={variationNames[i]} />
                    </div>
                )
            })}
        </div>
    )
}

// TODO add loading screen
function PlayersOpeningCharts({ name, url }) {

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

        return(
            <div>
                {(() => {
                    let charts = []
                    for (const eco in data["data"]) {
                        charts.push(<GenerateCharts data={data} eco={eco} name={name} />)
                    }
                    return charts
                })()}
            </div>
        )
        
    }
}

export default PlayersOpeningCharts;