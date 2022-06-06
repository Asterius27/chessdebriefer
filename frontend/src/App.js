import { Routes, Route, Navigate } from "react-router-dom";
import './App.css';
import MyNavbar from "./components/Navbar";
import Players from "./components/Players";
import Upload from "./components/Upload";
import Openings from "./components/Openings";
import Compares from "./components/Compares";
import Demo from "./components/Demo";
import Endgames from "./components/Endgames";
import Accuracy from "./components/Accuracy";
import ThrowsComebacks from "./components/ThrowsComebacks";
import EndgamesCompare from "./components/EndgamesCompare";
import GeneratePDF from "./components/GeneratePDF";

function App() {
  return (
    <div className="App">
      <MyNavbar />
      <Routes>
        <Route exact path="/" element={<Navigate to="/player" replace />}></Route>
        <Route exact path="/player" element={<Players />} />
        <Route exact path="/compare" element={<Compares />} />
        <Route exact path="/demo" element={<Demo />} />
        <Route exact path="/endgames" element={<Endgames />} />
        <Route exact path="/endgames/compare" element={<EndgamesCompare />} />
        <Route exact path="/throws-comebacks" element={<ThrowsComebacks />} />
        <Route exact path="/accuracy" element={<Accuracy />} />
        <Route exact path="/openings" element={<Openings />} />
        <Route exact path="/upload" element={<Upload />} />
        <Route exact path="/report" element={<GeneratePDF />} />
      </Routes>
    </div>
  );
}

export default App;
