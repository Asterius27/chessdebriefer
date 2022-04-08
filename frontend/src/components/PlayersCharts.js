import { useEffect, useState } from 'react';
import { DoughnutChart } from './ChartDoughnut';
import LoadingSpinner from './LoadingSpinner';

function PlayersCharts({ name, url }) {

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

    let sectionChartsData = []
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
        }
    }

    const doughnutStyle = {
      margin: "auto",
      paddingBottom: "7%",
      width: "40%",
      height: "40%"
    }

    return (
      <div>
        {sectionChartsData.map(function(sectionChartData, i){
            return (
                <div key={sectionNames[i]} style={doughnutStyle}>
                    <DoughnutChart chartData={sectionChartData} text={name + "'s " + sectionNames[i] + " wdls"} />
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

export default PlayersCharts;
