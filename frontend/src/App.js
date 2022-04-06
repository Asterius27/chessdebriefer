import { Routes, Route } from "react-router-dom";
import './App.css';
import Navbar from "./components/Navbar";
import Players from "./components/Players";
import Upload from "./components/Upload";
import Openings from "./components/Openings";
import Compares from "./components/Compares";
import Demo from "./components/Demo";
import Endgames from "./components/Endgames";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Players />} />
        <Route exact path="/compare" element={<Compares />} />
        <Route exact path="/demo" element={<Demo />} />
        <Route exact path="/endgames" element={<Endgames />} />
        <Route exact path="/openings" element={<Openings />} />
        <Route exact path="/upload" element={<Upload />} />
      </Routes>
    </div>
  );
}

export default App;
