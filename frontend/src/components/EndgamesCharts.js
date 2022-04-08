import { useEffect, useState } from 'react';
import { BarChart } from './ChartBar';
import LoadingSpinner from './LoadingSpinner';

function EndgamesCharts({ name, url }) {

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
    
        let predicted_wins = "matches you should have won (material advantage)"
        let predicted_losses = "matches you should have lost (material disadvantage)"
        let predicted_draws = "draws with material disadvantage"
        if (url.includes("tablebase")) {
            predicted_wins = "matches you should have won"
            predicted_losses = "matches you should have lost"
            predicted_draws = "matches you should have drawn"
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
    
        const barStyle = {
            margin: "auto",
            paddingBottom: "7%",
            width: "40%",
            height: "40%"
        }
    
        return (
            <div style={barStyle}>
                <BarChart chartData={chartData} text={name + "'s endgames stats"} />
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

export default EndgamesCharts;