import { useState } from "react";
import EndgamesCompareGeneralCharts from "./EndgamesCompareGeneralCharts";
import EndgamesCompareCharts from "./EndgamesCompareCharts";

// TODO check date format
function EndgamesCompare() {

    const [elo, setElo] = useState("")
    const [range, setRange] = useState("")
    const [section, setSection] = useState("")
    const [name, setName] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let eloQuery = "", rQuery = ""
        if (name) {
            let url = "http://localhost:8000/" + name + "/percentages/endgames"
            if (section) {
                url = url + "/" + section + "/compare"
            }
            else {
                url = url + "/compare"
            }
            if (elo) {
                eloQuery = "elo=" + elo + "&"
            }
            if (range) {
                rQuery = "range=" + range + "&"
            }
            if (eloQuery || rQuery) {
                url = url + "?" + eloQuery + rQuery
            }
            setUrl(url)
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div>
                {section ? 
                <div>
                    <EndgamesCompareCharts name={name} url={url} />
                </div> :
                <div>
                    <EndgamesCompareGeneralCharts name={name} url={url} />
                </div>
                }
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setName(""); setElo(""); setRange(""); setSection(""); e.preventDefault();}}>Back</button>
                </div>
            </div>
        )
    }
    else {
        return (
            <div>
                <form onSubmit={submitForm}>
                    <label>
                        Player Name:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="text"
                            onChange={(e) => setName(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Choose section:
                        <select style={{marginLeft: "7px"}} value={section} onChange={(e) => setSection(e.target.value)}>
                            <option value="">General</option>
                            <option value="material">Material</option>
                            <option value="tablebase">Tablebase (Slow)</option>
                        </select>
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Elo to compare to:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="number"
                            onChange={(e) => setElo(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Range:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="number"
                            onChange={(e) => setRange(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }
}

export default EndgamesCompare;