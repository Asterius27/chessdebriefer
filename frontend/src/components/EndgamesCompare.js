import { useState } from "react";
import EndgamesCompareGeneralCharts from "./EndgamesCompareGeneralCharts";
import EndgamesCompareCharts from "./EndgamesCompareCharts";
import EndgamesCompareWDLCharts from "./EndgamesCompareWDLCharts";
import EndgamesComparePredictedWDLCharts from "./EndgamesComparePredictedWDLCharts";

function EndgamesCompare() {

    const [minElo, setMinElo] = useState("")
    const [maxElo, setMaxElo] = useState("")
    const [elo, setElo] = useState("")
    const [range, setRange] = useState("")
    const [section, setSection] = useState("")
    const [name, setName] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let eloQuery = "", rQuery = "", minQuery = "", maxQuery = ""
        if (name) {
            let url = process.env.REACT_APP_BACKEND_URL + name + "/percentages/endgames"
            if (section) {
                url = url + "/" + section + "/compare"
            }
            else {
                url = url + "/compare"
            }
            if (minElo) {
                minQuery = "minelo=" + minElo + "&"
            }
            if (maxElo) {
                maxQuery = "maxelo=" + maxElo + "&"
            }
            if (elo) {
                eloQuery = "elo=" + elo + "&"
            }
            if (range) {
                rQuery = "range=" + range + "&"
            }
            if (eloQuery || rQuery || maxQuery || minQuery) {
                url = url + "?" + minQuery + maxQuery + eloQuery + rQuery
            }
            setUrl(url)
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div className="bg-light">
                {section ? <>
                    {section === "material/wdl" ? 
                    <div>
                        <EndgamesCompareWDLCharts name={name} url={url} />
                    </div> : 
                    <>
                        {section === "material/predicted" || section === "tablebase/predicted" ? 
                        <div>
                            <EndgamesComparePredictedWDLCharts name={name} url={url} />
                        </div> : 
                        <div>
                            <EndgamesCompareCharts name={name} url={url} />
                        </div>
                        } 
                    </>
                    }
                </> :
                <div>
                    <EndgamesCompareGeneralCharts name={name} url={url} />
                </div>
                }
                <div style={{paddingBottom: "2%"}}>
                    <button className="btn btn-primary" onClick={(e) => {setUrl(""); setName(""); setElo(""); setRange(""); setSection(""); setMaxElo(""); setMinElo(""); e.preventDefault();}}>Back</button>
                </div>
            </div>
        )
    }
    else {
        return (
            <div className="bg-light" style={{paddingBottom: "1%"}}>
                <form onSubmit={submitForm} style={{width: "80%", height: "80%", margin: "auto"}}>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="playername" style={{float: "left"}}>Player Name:</label>
                        <input className="form-control" id="playername" placeholder="Enter player name" type="text" onChange={(e) => setName(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="choosesection" style={{float: "left"}}>Choose section:</label>
                        <select id="choosesection" className="form-select" value={section} onChange={(e) => setSection(e.target.value)}>
                            <option value="">General</option>
                            <option value="material">Material</option>
                            <option value="material/wdl">Material WDL</option>
                            <option value="material/predicted">Material Predicted WDL</option>
                            <option value="tablebase">Tablebase (Slow)</option>
                            <option value="tablebase/predicted">Tablebase Predicted WDL</option>
                        </select>
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="minelo" style={{float: "left"}}>Player minimum elo:</label>
                        <input id="minelo" className="form-control" placeholder="Enter elo" type="number" onChange={(e) => setMinElo(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="maxelo" style={{float: "left"}}>Player maximum elo:</label>
                        <input id="maxelo" className="form-control" placeholder="Enter elo" type="number" onChange={(e) => setMaxElo(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="elo" style={{float: "left"}}>Elo to compare to:</label>
                        <input id="elo" className="form-control" placeholder="Enter elo" type="number" onChange={(e) => setElo(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="range" style={{float: "left"}}>Range:</label>
                        <input id="range" className="form-control" placeholder="Enter range" type="number" onChange={(e) => setRange(e.target.value)} />
                    </div>
                    <br/>
                    <input type="submit" value="Submit" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}

export default EndgamesCompare;