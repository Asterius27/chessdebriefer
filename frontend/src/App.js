import { Routes, Route } from "react-router-dom";
import './App.css';
import Percentages from "./components/Percentages";
import Navbar from "./components/Navbar";
import Upload from "./components/Upload";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Percentages />} />
        <Route exact path="/upload" element={<Upload />} />
      </Routes>
    </div>
  );
}

export default App;
