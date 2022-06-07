import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';
import LoadingSpinner from './LoadingSpinner';

function EndgamesWDLCharts({ name, url, onLoad }) {

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
    
        let advantageChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [data["data"]["material advantage"]["wins"], data["data"]["material advantage"]["losses"], data["data"]["material advantage"]["draws"]],
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
                data: [data["data"]["material disadvantage"]["wins"], data["data"]["material disadvantage"]["losses"], data["data"]["material disadvantage"]["draws"]],
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

        if (onLoad) {
            onLoad(true, url);
        }
    
        return (
            <div>
                {data["data"]["material advantage"]["wins"] + data["data"]["material advantage"]["losses"] + data["data"]["material advantage"]["draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={advantageChartData} text={name + " material advantage wdl endgame stats"} />
                </div> : <div></div>
                }
                {data["data"]["material disadvantage"]["wins"] + data["data"]["material disadvantage"]["losses"] + data["data"]["material disadvantage"]["draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={disadvantageChartData} text={name + " material disadvantage wdl endgame stats"} />
                </div> : <div></div>
                }
            </div>
        )
    
    } else {
        return (
            <LoadingSpinner />
        )
    }

}

export default EndgamesWDLCharts;