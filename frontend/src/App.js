import { Routes, Route } from "react-router-dom";
import './App.css';
import Percentages from "./components/Percentages";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Percentages />} />
      </Routes>
    </div>
  );
}

export default App;
