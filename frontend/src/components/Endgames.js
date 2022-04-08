import { useState } from "react";
import EndgamesCharts from "./EndgamesCharts";
import EndgamesGeneralCharts from "./EndgamesGeneralCharts";
import EndgamesWDLCharts from "./EndgamesWDLCharts";

function Endgames() {

    const [opponent, setOpponent] = useState("")
    const [from, setFrom] = useState("")
    const [to, setTo] = useState("")
    const [minElo, setMinElo] = useState("")
    const [maxElo, setMaxElo] = useState("")
    const [pieces, setPieces] = useState("")
    const [name, setName] = useState("")
    const [section, setSection] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let oQuery = "", fQuery = "", tQuery = "", minQuery = "", maxQuery = "", pQuery = ""
        if (name) {
            let url = "http://localhost:8000/" + name + "/percentages/endgames"
            if (section) {
                url = url + "/" + section
            }
            if (opponent) {
                oQuery = "opponent=" + opponent + "&"
            }
            if (from) {
                fQuery = "from=" + from + "&"
            }
            if (to) {
                tQuery = "to=" + to + "&"
            }
            if (minElo) {
                minQuery = "minelo=" + minElo + "&"
            }
            if (maxElo) {
                maxQuery = "maxelo=" + maxElo + "&"
            }
            if (pieces) {
                pQuery = "pieces=" + pieces + "&"
            }
            if (oQuery || fQuery || tQuery || minQuery || maxQuery || pQuery ) {
                url = url + "?" + oQuery + fQuery + tQuery + minQuery + maxQuery + pQuery
            }
            setUrl(url)
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div>
                {section ? <>
                    {section === "material/wdl" ? 
                    <div>
                        <EndgamesWDLCharts name={name} url={url} />
                    </div> : 
                    <div>
                        <EndgamesCharts name={name} url={url} />
                    </div>
                    }
                </> :
                <div>
                    <EndgamesGeneralCharts name={name} url={url} />
                </div>
                }
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); setSection(""); setPieces(""); e.preventDefault();}}>Back</button>
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
                            <option value="material/wdl">Material WDL</option>
                            <option value="tablebase">Tablebase</option>
                        </select>
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Only use matches against this opponent:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="text"
                            onChange={(e) => setOpponent(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Min Elo:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="number"
                            onChange={(e) => setMinElo(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Max Elo:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="number"
                            onChange={(e) => setMaxElo(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Only use matches played after this date:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="date"
                            onChange={(e) => setFrom(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Only use matches played before this date:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="date"
                            onChange={(e) => setTo(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        How many pieces must be left on the board to be considered an endgame:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="number"
                            onChange={(e) => setPieces(e.target.value)}
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

export default Endgames;