import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';

function PlayersGeneralCharts({ name, url }) {

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

    const doughnutStyle = {
      margin: "auto",
      paddingBottom: "7%",
      width: "40%",
      height: "40%"
    }

    return (
      <div>
        {data["data"]["general percentages"]["your wins"] + data["data"]["general percentages"]["your losses"] + data["data"]["general percentages"]["your draws"] !== 0 ? 
          <div style={doughnutStyle}>
            <DoughnutChart chartData={generalChartData} text={name + " general wdl stats"} />
          </div> : <div></div>
        }
        {data["data"]["side percentages"]["white"]["your wins"] + data["data"]["side percentages"]["white"]["your losses"] + data["data"]["side percentages"]["white"]["your draws"] !== 0 ? 
          <div style={doughnutStyle}>
            <DoughnutChart chartData={whiteChartData} text={name + " white wdl stats"} />
          </div> : <div></div>
        }
        {data["data"]["side percentages"]["black"]["your wins"] + data["data"]["side percentages"]["black"]["your losses"] + data["data"]["side percentages"]["black"]["your draws"] !== 0 ? 
          <div style={doughnutStyle}>
            <DoughnutChart chartData={blackChartData} text={name + " black wdl stats"} />
          </div> : <div></div>
        }
      </div>
    )

  }
    
}

export default PlayersGeneralCharts;
