import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';
import LoadingSpinner from './LoadingSpinner';

function ComparesCharts({ name, url }) {

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

    let sectionChartsData = []
    let compareSectionChartsData = []
    let sectionNames = []
    for (const section in data["data"]) {
        if (data["data"][section]["your wins"] + data["data"][section]["your losses"] + data["data"][section]["your draws"] !== 0) {
            sectionNames.push(section)
            sectionChartsData.push({
                labels: ['Wins', 'Losses', 'Draws'],
                datasets: [{
                    label: 'wdl',
                    data: [data["data"][section]["your wins"], data["data"][section]["your losses"], data["data"][section]["your draws"]],
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                    ],
                    hoverOffset: 4
                }]
            })
            compareSectionChartsData.push({
                labels: ['Wins', 'Losses', 'Draws'],
                datasets: [{
                    label: 'wdl',
                    data: [data["data"][section]["other players wins"], data["data"][section]["other players losses"], data["data"][section]["other players draws"]],
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                    ],
                    hoverOffset: 4
                }]
            })
        }
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
        {sectionChartsData.map(function(sectionChartData, i){
            return (
                <div key={sectionNames[i]} style={{display: "table-row"}}>
                    <div style={doughnutStyle}>
                        <DoughnutChart chartData={sectionChartData} text={name + "'s " + sectionNames[i] + " wdls"} />
                    </div>
                    <div style={doughnutStyle}>
                        <DoughnutChart chartData={compareSectionChartsData[i]} text={"Other player's " + sectionNames[i] + " wdls"} />
                    </div>
                </div>
            )
        })}
      </div>
    )

  } else {
    return (
      <LoadingSpinner />
    )
  }
    
}

export default ComparesCharts;
