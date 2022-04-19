import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';
import LoadingSpinner from './LoadingSpinner';

function EndgamesPredictedWDLCharts({ name, url, generalUrl }) {

    useEffect(() => {
        const fetchPercentages = async () => {
            const res = await fetch(url).catch(err => {alert("An error has occured, please go back and try again")})
            const data = await res.json()
            setData({ data: data })
            const res2 = await fetch(generalUrl).catch(err => {alert("An error has occured, please go back and try again")})
            const data2 = await res2.json()
            setGeneralData({ data: data2 })
        }
        fetchPercentages()
    }, []);
    
    const [data, setData] = useState({})
    const [generalData, setGeneralData] = useState({})
    
    if (Object.keys(data).length !== 0 && Object.keys(generalData).length !== 0) {
    
        let predictedGeneralChartData = {
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
    
        let predictedWhiteChartData = {
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
    
        let predictedBlackChartData = {
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

        let generalChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'wdl',
                data: [generalData["data"]["general percentages"]["wins"], generalData["data"]["general percentages"]["losses"], generalData["data"]["general percentages"]["draws"]],
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
                data: [generalData["data"]["side percentages"]["white"]["wins"], generalData["data"]["side percentages"]["white"]["losses"], generalData["data"]["side percentages"]["white"]["draws"]],
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
                data: [generalData["data"]["side percentages"]["black"]["wins"], generalData["data"]["side percentages"]["black"]["losses"], generalData["data"]["side percentages"]["black"]["draws"]],
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

            <div>
                <div style={{margin: "auto", width: "80%", display: "table"}}>
                    <div style={{display: "table-row"}}>
                        {generalData["data"]["general percentages"]["wins"] + generalData["data"]["general percentages"]["losses"] + generalData["data"]["general percentages"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={generalChartData} text={name + " general wdl endgame stats"} />
                        </div> : <div></div>
                        }
                        {data["data"]["general percentages"]["wins"] + data["data"]["general percentages"]["losses"] + data["data"]["general percentages"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={predictedGeneralChartData} text={"Predicted general wdl endgame stats"} />
                        </div> : <div></div>
                        }
                    </div>
                    <div style={{display: "table-row"}}>
                        {generalData["data"]["side percentages"]["white"]["wins"] + generalData["data"]["side percentages"]["white"]["losses"] + generalData["data"]["side percentages"]["white"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={whiteChartData} text={name + " white wdl endgame stats"} />
                        </div> : <div></div>
                        }
                        {data["data"]["side percentages"]["white"]["wins"] + data["data"]["side percentages"]["white"]["losses"] + data["data"]["side percentages"]["white"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={predictedWhiteChartData} text={"Predicted white wdl endgame stats"} />
                        </div> : <div></div>
                        }
                    </div>
                    <div style={{display: "table-row"}}>
                        {generalData["data"]["side percentages"]["black"]["wins"] + generalData["data"]["side percentages"]["black"]["losses"] + generalData["data"]["side percentages"]["black"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={blackChartData} text={name + " black wdl endgame stats"} />
                        </div> : <div></div>
                        }
                        {data["data"]["side percentages"]["black"]["wins"] + data["data"]["side percentages"]["black"]["losses"] + data["data"]["side percentages"]["black"]["draws"] !== 0 ? 
                        <div style={doughnutStyle}>
                            <DoughnutChart chartData={predictedBlackChartData} text={"Predicted black wdl endgame stats"} />
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

export default EndgamesPredictedWDLCharts;