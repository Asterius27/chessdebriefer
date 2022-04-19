import { useEffect, useState } from 'react';
import { BarChart } from './ChartBar';
import { DoughnutChart } from './ChartDoughnut';
import { StackedBarChart } from './ChartStackedBar';
import LoadingSpinner from './LoadingSpinner';

function PlayersCharts({ name, url }) {

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
    let sectionNames = []
    let matchesPlayed = []
    let wins = []
    let losses = []
    let draws = []
    for (const section in data["data"]) {
        if (data["data"][section]["your wins"] + data["data"][section]["your losses"] + data["data"][section]["your draws"] !== 0) {
            sectionNames.push(section)
            matchesPlayed.push(data["data"][section]["your wins"] + data["data"][section]["your losses"] + data["data"][section]["your draws"])
            wins.push(data["data"][section]["your wins"])
            losses.push(data["data"][section]["your losses"])
            draws.push(data["data"][section]["your draws"])
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

    let barChartData = {
      labels: sectionNames,
      datasets: [{
        label: 'matches played',
        data: matchesPlayed,
        backgroundColor: 'rgb(50, 205, 50)',
        hoverOffset: 4
      }]
    }

    let stackedBarChartData = {
      labels: sectionNames,
      datasets: [{
        label: 'wins',
        data: wins,
        backgroundColor: 'rgb(255, 99, 132)',
        hoverOffset: 4
      }, {
        label: 'losses',
        data: losses,
        backgroundColor: 'rgb(54, 162, 235)',
        hoverOffset: 4
      }, {
        label: 'draws',
        data: draws,
        backgroundColor: 'rgb(255, 205, 86)',
        hoverOffset: 4
      }]
    }

    const doughnutStyle = {
      margin: "auto",
      paddingBottom: "7%",
      width: "40%",
      height: "40%"
    }

    const barStyle = {
      margin: "auto",
      paddingBottom: "7%",
      width: "70%",
      height: "40%"
    }

    return (
      <div>
        <div style={barStyle}>
          <BarChart chartData={barChartData} text={name + "'s most played"} />
        </div>
        <div style={barStyle}>
          <StackedBarChart chartData={stackedBarChartData} text={name + "'s most played"} />
        </div>
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
