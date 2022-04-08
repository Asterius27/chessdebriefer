import { useEffect, useState } from 'react';
import { BarChart } from './ChartBar';

function ThrowsComebacksCharts({ name, url }) {

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

        let chartData = {
            labels: ['Wins', 'Losses'],
            datasets: [{
                label: 'Your Stats',
                data: [data["data"]["wins"], data["data"]["losses"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)'
                ],
                hoverOffset: 4
            },
            {
                label: 'Engine Predictions',
                data: [data["data"]["comebacks"], data["data"]["throws"]],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)'
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
                <BarChart chartData={chartData} text={name + "'s throws-comebacks"} />
                <p>Throws are the matches you lost while having engine advantage for most of the time and comebacks are the matches you won while having engine disadvantage for most of the time</p>
            </div>
        )
    
    }
}

export default ThrowsComebacksCharts;