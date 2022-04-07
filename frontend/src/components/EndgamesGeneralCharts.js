import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';

function EndgamesGeneralCharts({ name, url }) {

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
    
        const doughnutStyle = {
            margin: "auto",
            paddingBottom: "7%",
            width: "40%",
            height: "40%"
        }
    
        return (
            <div>
                <h3>You have played {data["data"]["general percentages"]["games"]} of which {data["data"]["general percentages"]["endgames"]} ({data["data"]["general percentages"]["percentage of games that finish in the endgame"]} %) reached the endgame</h3>
                {data["data"]["general percentages"]["wins"] + data["data"]["general percentages"]["losses"] + data["data"]["general percentages"]["draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={generalChartData} text={name + " general wdl endgame stats"} />
                </div> : <div></div>
                }
                {data["data"]["side percentages"]["white"]["wins"] + data["data"]["side percentages"]["white"]["losses"] + data["data"]["side percentages"]["white"]["draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={whiteChartData} text={name + " white wdl endgame stats"} />
                </div> : <div></div>
                }
                {data["data"]["side percentages"]["black"]["wins"] + data["data"]["side percentages"]["black"]["losses"] + data["data"]["side percentages"]["black"]["draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={blackChartData} text={name + " black wdl endgame stats"} />
                </div> : <div></div>
                }
            </div>
        )
    
    }

}

export default EndgamesGeneralCharts;