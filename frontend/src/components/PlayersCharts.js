import { useEffect, useState } from 'react';
import { StackedBarChart } from './ChartStackedBar';
import LoadingSpinner from './LoadingSpinner';

function PlayersCharts({ name, url, onLoad, section }) {

  useEffect(() => {
    const fetchPercentages = async () => {
      const res = await fetch(url).catch(err => {alert("An error has occured, please go back and try again")})
      const data = await res.json()
      setData({ data: data })
    }
    fetchPercentages()
  }, []);

  const [data, setData] = useState({})
  let flag = false

  if (Object.keys(data).length !== 0) {

    let sectionNames = []
    let wins = []
    let losses = []
    let draws = []
    let win_percentages = []
    let loss_percentages = []
    let draw_percentages = []
    for (const section in data["data"]) {
        if (data["data"][section]["your wins"] + data["data"][section]["your losses"] + data["data"][section]["your draws"] !== 0) {
            sectionNames.push(section)
            wins.push(data["data"][section]["your wins"])
            losses.push(data["data"][section]["your losses"])
            draws.push(data["data"][section]["your draws"])
            win_percentages.push(data["data"][section]["your win percentage"])
            loss_percentages.push(data["data"][section]["your loss percentage"])
            draw_percentages.push(data["data"][section]["your draw percentage"])
        }
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

    let stackedPercentagesBarChart = {
      labels: sectionNames,
      datasets: [{
        label: 'win percentage',
        data: win_percentages,
        backgroundColor: 'rgb(255, 99, 132)',
        hoverOffset: 4
      }, {
        label: 'loss percentage',
        data: loss_percentages,
        backgroundColor: 'rgb(54, 162, 235)',
        hoverOffset: 4
      }, {
        label: 'draw percentage',
        data: draw_percentages,
        backgroundColor: 'rgb(255, 205, 86)',
        hoverOffset: 4
      }]
    }

    const barStyle = {
      margin: "auto",
      paddingBottom: "7%",
      width: "70%",
      height: "40%"
    }

    if (onLoad) {
      onLoad(true, url);
      flag = true
    }

    if (!section) {
      section = "";
    } else {
      section = " " + section;
    }

    return (
      <div>
        <div style={barStyle}>
          <StackedBarChart chartData={stackedBarChartData} text={name + "'s" + section + " wdl stats"} displayLabels={flag} />
        </div>
        <div style={barStyle}>
          <StackedBarChart chartData={stackedPercentagesBarChart} text={name + "'s" + section + " wdl stats"} displayLabels={flag} />
        </div>
      </div>
    )

  } else {
    return (
      <LoadingSpinner />
    )
  }
    
}

export default PlayersCharts;
