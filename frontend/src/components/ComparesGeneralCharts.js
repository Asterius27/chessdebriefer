import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';
import LoadingSpinner from './LoadingSpinner';

function ComparesGeneralCharts({ name, url }) {

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
        data: [data["data"]["general percentages"]["your wins"], data["data"]["general percentages"]["your losses"], data["data"]["general percentages"]["your draws"]],
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

    let whiteChartData = {
      labels: ['Wins', 'Losses', 'Draws'],
      datasets: [{
        label: 'wdl',
        data: [data["data"]["side percentages"]["white"]["your wins"], data["data"]["side percentages"]["white"]["your losses"], data["data"]["side percentages"]["white"]["your draws"]],
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

    let blackChartData = {
      labels: ['Wins', 'Losses', 'Draws'],
      datasets: [{
        label: 'wdl',
        data: [data["data"]["side percentages"]["black"]["your wins"], data["data"]["side percentages"]["black"]["your losses"], data["data"]["side percentages"]["black"]["your draws"]],
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

    return (
        <div style={{margin: "auto", width: "80%", display: "table"}}>
            <div style={{display: "table-row"}}>
                {data["data"]["general percentages"]["your wins"] + data["data"]["general percentages"]["your losses"] + data["data"]["general percentages"]["your draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={generalChartData} text={name + "'s general wdl stats"} />
                </div> : <div></div>
                }
                {data["data"]["general percentages"]["other players wins"] + data["data"]["general percentages"]["other players losses"] + data["data"]["general percentages"]["other players draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={compareGeneralChartData} text={"Other players general wdl stats"} />
                </div> : <div></div>
                }
            </div>
            <div style={{display: "table-row"}}>
                {data["data"]["side percentages"]["white"]["your wins"] + data["data"]["side percentages"]["white"]["your losses"] + data["data"]["side percentages"]["white"]["your draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={whiteChartData} text={name + "'s white wdl stats"} />
                </div> : <div></div>
                }
                {data["data"]["side percentages"]["white"]["other players wins"] + data["data"]["side percentages"]["white"]["other players losses"] + data["data"]["side percentages"]["white"]["other players draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={compareWhiteChartData} text={"Other player's white wdl stats"} />
                </div> : <div></div>
                }
            </div>
            <div style={{display: "table-row"}}>
                {data["data"]["side percentages"]["black"]["your wins"] + data["data"]["side percentages"]["black"]["your losses"] + data["data"]["side percentages"]["black"]["your draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={blackChartData} text={name + "'s black wdl stats"} />
                </div> : <div></div>
                }
                {data["data"]["side percentages"]["black"]["other players wins"] + data["data"]["side percentages"]["black"]["other players losses"] + data["data"]["side percentages"]["black"]["other players draws"] !== 0 ? 
                <div style={doughnutStyle}>
                    <DoughnutChart chartData={compareBlackChartData} text={"Other player's black wdl stats"} />
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

export default ComparesGeneralCharts;
