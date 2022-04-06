import { Routes, Route } from "react-router-dom";
import './App.css';
import Navbar from "./components/Navbar";
import Players from "./components/Players";
import Upload from "./components/Upload";
import Openings from "./components/Openings";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Players />} />
        <Route exact path="/upload" element={<Upload />} />
        <Route exact path="/openings" element={<Openings />} />
      </Routes>
    </div>
  );
}

export default App;
