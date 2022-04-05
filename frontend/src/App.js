import { Routes, Route } from "react-router-dom";
import './App.css';
import Percentages from "./components/Percentages";
import Navbar from "./components/Navbar";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Percentages />} />
      </Routes>
    </div>
  );
}

export default App;
