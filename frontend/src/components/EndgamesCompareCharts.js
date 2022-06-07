import { useEffect, useState } from 'react';
import { BarChart } from './ChartBar';
import LoadingSpinner from './LoadingSpinner';

function EndgamesCompareCharts({ name, url, onLoad, section }) {

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
    
        let predicted_wins = "matches you should have won (material advantage)"
        let predicted_losses = "matches you should have lost (material disadvantage)"
        let predicted_draws = "draws with material disadvantage"
        if (url.includes("tablebase")) {
            predicted_wins = "matches you should have won"
            predicted_losses = "matches you should have lost"
            predicted_draws = "matches you should have drawn"
        }

        let other_predicted_wins = "matches other players should have won (material advantage)"
        let other_predicted_losses = "matches other players should have lost (material disadvantage)"
        let other_predicted_draws = "other players draws with material disadvantage"
        if (url.includes("tablebase")) {
            other_predicted_wins = "matches other players should have won"
            other_predicted_losses = "matches other players should have lost"
            other_predicted_draws = "matches other players should have drawn"
        }

        let chartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'your wdl stat',
                data: [data["data"]["wins"], data["data"]["losses"], data["data"]["draws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            },
            {
                label: 'predicted wdl stat',
                data: [data["data"][predicted_wins], data["data"][predicted_losses], data["data"][predicted_draws]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }

        let compareChartData = {
            labels: ['Wins', 'Losses', 'Draws'],
            datasets: [{
                label: 'other players wdl stat',
                data: [data["data"]["other players wins"], data["data"]["other players losses"], data["data"]["other players draws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            },
            {
                label: 'other players predicted wdl stat',
                data: [data["data"][other_predicted_wins], data["data"][other_predicted_losses], data["data"][other_predicted_draws]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        }
    
        const barStyle = {
            margin: "auto",
            paddingBottom: "7%",
            paddingLeft: "2%",
            paddingRight: "2%",
            width: "50%",
            height: "50%",
            display: "table-cell"
        }

        if (onLoad) {
            onLoad(true, url);
            flag = true;
        }

        if (!section) {
            section = "";
        } else {
            section = " " + section;
        }
    
        return (
            <div>
                <div style={{margin: "auto", width: "90%", display: "table"}}>
                    <div style={{display: "table-row"}}>
                        <div style={barStyle}>
                            <BarChart chartData={chartData} text={name + "'s" + section + " endgames stats"} displayLabels={flag} />
                        </div>
                        <div style={barStyle}>
                            <BarChart chartData={compareChartData} text={"other players" + section + " endgames stats"} displayLabels={flag} />
                        </div>
                    </div>
                </div>
                {url.includes("tablebase") ? 
                <p>The predicted wdl stat indicates how many of those wins/losses/draws you should have gotten according to the tablebase</p> :
                <p>The predicted wdl stat indicates how many of those wins/losses/draws you should have gotten based on material advantage (for the wins) or material disadvantage (for the losses). 
                    As for the draws it only shows how many matches you drew with material disadvantage</p>}
            </div>
        )
    
    } else {
        return (
            <LoadingSpinner />
        )
    }
}

export default EndgamesCompareCharts;