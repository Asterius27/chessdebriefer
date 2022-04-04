import { useEffect, useState } from 'react';
import { DoughnutChart } from './components/Chart';
import './App.css';

function App() {

  useEffect(() => {
    const fetchPercentages = async () => {
      const name = "mamalak"
      const res = await fetch("http://localhost:8000/" + name + "/percentages")
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
      'padding-bottom': "7%",
      width: "40%",
      height: "40%"
    }

    return (
      <div className='App'>
        <div style={doughnutStyle}>
          <DoughnutChart chartData={generalChartData} text={"Your general wdl stats"} />
        </div>
        <div style={doughnutStyle}>
          <DoughnutChart chartData={whiteChartData} text={"Your white wdl stats"} />
        </div>
        <div style={doughnutStyle}>
          <DoughnutChart chartData={blackChartData} text={"Your black wdl stats"} />
        </div>
      </div>
    )

  }
    
}

export default App;
