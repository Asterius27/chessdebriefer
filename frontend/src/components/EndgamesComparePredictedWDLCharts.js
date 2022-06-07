import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';
import LoadingSpinner from './LoadingSpinner';

function EndgamesComparePredictedWDLCharts({ name, url, onLoad }) {

    useEffect(() => {
        const fetchPercentages = async () => {
            const res = await fetch(url).catch(err => {alert("An error has occured, please go back and try again")})
            const data = await res.json()
            setData({ data: data })
        }
        fetchPercentages()
    }, []);
    
    const [data, setData] = useState({})
    
    if (Object.keys(data).length !== 0) {
    
        let generalChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["general percentages"]["wins"], data["data"]["general percentages"]["losses"], data["data"]["general percentages"]["draws"]],
                backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    
        let whiteChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["side percentages"]["white"]["wins"], data["data"]["side percentages"]["white"]["losses"], data["data"]["side percentages"]["white"]["draws"]],
                backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    
        let blackChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["side percentages"]["black"]["wins"], data["data"]["side percentages"]["black"]["losses"], data["data"]["side percentages"]["black"]["draws"]],
                backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }

        let compareGeneralChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["general percentages"]["other players wins"], data["data"]["general percentages"]["other players losses"], data["data"]["general percentages"]["other players draws"]],
                backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    
        let compareWhiteChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["side percentages"]["white"]["other players wins"], data["data"]["side percentages"]["white"]["other players losses"], data["data"]["side percentages"]["white"]["other players draws"]],
                backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    
        let compareBlackChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["side percentages"]["black"]["other players wins"], data["data"]["side percentages"]["black"]["other players losses"], data["data"]["side percentages"]["black"]["other players draws"]],
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

        if (onLoad) {
            onLoad(true, url);
        }
    
        return (

            <div>
                <div style={{margin: "auto", width: "80%", display: "table"}}>
                    <div style={{display: "table-row"}}>
                        {data["data"]["general percentages"]["wins"] + data["data"]["general percentages"]["losses"] + data["data"]["general percentages"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={generalChartData} text={name + " predicted wdl endgame stats"} />
                        </div> : <div></div>
                        }
                        {data["data"]["general percentages"]["other players wins"] + data["data"]["general percentages"]["other players losses"] + data["data"]["general percentages"]["other players draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={compareGeneralChartData} text={"Other players predicted wdl endgame stats"} />
                        </div> : <div></div>
                        }
                    </div>
                    <div style={{display: "table-row"}}>
                        {data["data"]["side percentages"]["white"]["wins"] + data["data"]["side percentages"]["white"]["losses"] + data["data"]["side percentages"]["white"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={whiteChartData} text={name + " white predicted wdl endgame stats"} />
                        </div> : <div></div>
                        }
                        {data["data"]["side percentages"]["white"]["other players wins"] + data["data"]["side percentages"]["white"]["other players losses"] + data["data"]["side percentages"]["white"]["other players draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={compareWhiteChartData} text={"Other player's white predicted wdl endgame stats"} />
                        </div> : <div></div>
                        }
                    </div>
                    <div style={{display: "table-row"}}>
                        {data["data"]["side percentages"]["black"]["wins"] + data["data"]["side percentages"]["black"]["losses"] + data["data"]["side percentages"]["black"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={blackChartData} text={name + " black predicted wdl endgame stats"} />
                        </div> : <div></div>
                        }
                        {data["data"]["side percentages"]["black"]["other players wins"] + data["data"]["side percentages"]["black"]["other players losses"] + data["data"]["side percentages"]["black"]["other players draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={compareBlackChartData} text={"Other player's black predicted wdl endgame stats"} />
                        </div> : <div></div>
                        }
                    </div>
                </div>
            </div>
        )
    
    } else {
        return (
            <LoadingSpinner />
        )
    }

}

export default EndgamesComparePredictedWDLCharts;