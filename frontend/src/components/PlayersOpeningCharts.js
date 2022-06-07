import { useEffect, useState } from "react";
import { DoughnutChart } from "./ChartDoughnut";
import LoadingSpinner from "./LoadingSpinner";

function GenerateCharts({ data, eco, name, displayLabels }) {

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
                <h1 style={{fontSize: "600%"}}>{eco}</h1>
            </div>
            <div style={doughnutStyle}>
                <DoughnutChart chartData={generalChartData} text={name + "'s " + eco + " wdl"} displayLabels={displayLabels} />
            </div>
            {whiteChartData ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={whiteChartData} text={name + "'s " + eco + " white wdl"} displayLabels={displayLabels} />
                </div> : <div></div>
            }
            {blackChartData ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={blackChartData} text={name + "'s " + eco + " black wdl"} displayLabels={displayLabels} />
                </div> : <div></div>
            }
            <div>
                <h1 style={{fontSize: "400%"}}>Variations</h1>
            </div>
            {variationsChartsData.map(function(variationsChartData, i){
                return (
                    <div key={variationNames[i]} style={doughnutStyle}>
                        <DoughnutChart chartData={variationsChartData} text={variationNames[i]} displayLabels={displayLabels} />
                    </div>
                )
            })}
        </div>
    )
}

function PlayersOpeningCharts({ name, url, onLoad }) {

    useEffect(() => {
        const fetchPercentages = async () => {
            const res = await fetch(url).catch(err => {alert("An error has occured, please go back and try again")})
            const data = await res.json()
            setData({ data: data })
        }
        fetchPercentages()
    }, [])

    const [data, setData] = useState({})

    if (Object.keys(data).length !== 0) {

        let flag = false;
        
        if (onLoad) {
            onLoad(true, url);
            flag = true;
        }

        return(
            <div>
                {(() => {
                    let charts = []
                    for (const eco in data["data"]) {
                        charts.push(<GenerateCharts data={data} eco={eco} name={name} displayLabels={flag} />)
                    }
                    return charts
                })()}
            </div>
        )
        
    } else {
        return (
            <LoadingSpinner />
        )
    }
}

export default PlayersOpeningCharts;