import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';
import LoadingSpinner from './LoadingSpinner';

function EndgamesCompareWDLCharts({ name, url }) {

    useEffect(() => {
        const fetchPercentages = async () => {
            const res = await fetch(url)
            const data = await res.json()
            setData({ data: data })
        }
        fetchPercentages()
    }, []);
    
    const [data, setData] = useState({})
    
    if (Object.keys(data).length !== 0) {
    
        let advantageChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["your stats"]["material advantage"]["wins"], data["data"]["your stats"]["material advantage"]["losses"], data["data"]["your stats"]["material advantage"]["draws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    
        let disadvantageChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["your stats"]["material disadvantage"]["wins"], data["data"]["your stats"]["material disadvantage"]["losses"], data["data"]["your stats"]["material disadvantage"]["draws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }

        let compareAdvantageChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["other players stats"]["material advantage"]["wins"], data["data"]["other players stats"]["material advantage"]["losses"], data["data"]["other players stats"]["material advantage"]["draws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    
        let compareDisadvantageChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["other players stats"]["material disadvantage"]["wins"], data["data"]["other players stats"]["material disadvantage"]["losses"], data["data"]["other players stats"]["material disadvantage"]["draws"]],
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
            width: "50%",
            height: "50%",
            display: "table-cell"
        }
    
        return (
            <div style={{margin: "auto", width: "80%", display: "table"}}>
                <div style={{display: "table-row"}}>
                    {data["data"]["your stats"]["material advantage"]["wins"] + data["data"]["your stats"]["material advantage"]["losses"] + data["data"]["your stats"]["material advantage"]["draws"] !== 0 ? 
                    <div style={doughnutStyle}>
                        <DoughnutChart chartData={advantageChartData} text={name + " material advantage wdl endgame stats"} />
                    </div> : <div></div>
                    }
                    {data["data"]["other players stats"]["material advantage"]["wins"] + data["data"]["other players stats"]["material advantage"]["losses"] + data["data"]["other players stats"]["material advantage"]["draws"] !== 0 ? 
                    <div style={doughnutStyle}>
                        <DoughnutChart chartData={compareAdvantageChartData} text={"Other player's material advantage wdl endgame stats"} />
                    </div> : <div></div>
                    }
                </div>
                <div style={{display: "table-row"}}> 
                    {data["data"]["your stats"]["material disadvantage"]["wins"] + data["data"]["your stats"]["material disadvantage"]["losses"] + data["data"]["your stats"]["material disadvantage"]["draws"] !== 0 ? 
                    <div style={doughnutStyle}>
                        <DoughnutChart chartData={disadvantageChartData} text={name + " material disadvantage wdl endgame stats"} />
                    </div> : <div></div>
                    }
                    {data["data"]["other players stats"]["material disadvantage"]["wins"] + data["data"]["other players stats"]["material disadvantage"]["losses"] + data["data"]["other players stats"]["material disadvantage"]["draws"] !== 0 ? 
                    <div style={doughnutStyle}>
                        <DoughnutChart chartData={compareDisadvantageChartData} text={"Other player's material disadvantage wdl endgame stats"} />
                    </div> : <div></div>
                    }
                </div>
            </div>
        )
    
    } else {
        return (
            <LoadingSpinner />
        )
    }

}

export default EndgamesCompareWDLCharts;