import { Routes, Route } from "react-router-dom";
import './App.css';
import Navbar from "./components/Navbar";
import PlayerCharts from "./components/PlayerCharts";
import Upload from "./components/Upload";
import Openings from "./components/Openings";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route exact path="/" element={<PlayerCharts />} />
        <Route exact path="/upload" element={<Upload />} />
        <Route exact path="/openings" element={<Openings />} />
      </Routes>
    </div>
  );
}

export default App;
