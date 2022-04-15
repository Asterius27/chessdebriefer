import { Routes, Route } from "react-router-dom";
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

// TODO make it nicer with bootstrap, remove duplicate code, add error handling
function App() {
  return (
    <div className="App">
      <MyNavbar />
      <Routes>
        <Route exact path="/" element={<Players />} />
        <Route exact path="/compare" element={<Compares />} />
        <Route exact path="/demo" element={<Demo />} />
        <Route exact path="/endgames" element={<Endgames />} />
        <Route exact path="/endgames/compare" element={<EndgamesCompare />} />
        <Route exact path="/throws-comebacks" element={<ThrowsComebacks />} />
        <Route exact path="/accuracy" element={<Accuracy />} />
        <Route exact path="/openings" element={<Openings />} />
        <Route exact path="/upload" element={<Upload />} />
      </Routes>
    </div>
  );
}

export default App;
