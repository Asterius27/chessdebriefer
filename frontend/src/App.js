import { useEffect, useState } from 'react';
import { DoughnutChart } from './components/Chart';
// import logo from './logo.svg';
import './App.css';

function App() {

  useEffect(() => {
    const fetchPercentages = async () => {
      const name = "mamalak"
      const res = await fetch("http://localhost:8000/" + name + "/percentages")
      const data = await res.json()
      setChartData({
        labels: ['Wins', 'Losses', 'Draws'],
        datasets: [{
          label: 'wdl',
          data: [data["general percentages"]["your wins"], data["general percentages"]["your losses"], data["general percentages"]["your draws"]],
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      })
    }
    fetchPercentages()
  }, []);

  const [chartData, setChartData] = useState({})
  const doughnutStyle = {
    width: "40%",
    height: "40%"
  }

  if (Object.keys(chartData).length !== 0) {
    return (
      <div className='App'>
        <div style={doughnutStyle}>
          <DoughnutChart chartData={chartData} />
        </div>
      </div>
    )
  }
  /*
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
  */
}

export default App;
