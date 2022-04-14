import { useState } from "react";
import EndgamesCharts from "./EndgamesCharts";
import EndgamesGeneralCharts from "./EndgamesGeneralCharts";
import EndgamesWDLCharts from "./EndgamesWDLCharts";
import EndgamesPredictedWDLCharts from "./EndgamesPredictedWDLCharts";

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
    const [url2, setUrl2] = useState("")
    
    const submitForm = (e) => {
        let oQuery = "", fQuery = "", tQuery = "", minQuery = "", maxQuery = "", pQuery = ""
        if (name) {
            let url = "http://localhost:8000/" + name + "/percentages/endgames"
            let url2 = "http://localhost:8000/" + name + "/percentages/endgames"
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
            if (section === "tablebase/predicted") {
                pQuery = "pieces=5&"
            }
            if (oQuery || fQuery || tQuery || minQuery || maxQuery || pQuery ) {
                url = url + "?" + oQuery + fQuery + tQuery + minQuery + maxQuery + pQuery
                url2 = url2 + "?" + oQuery + fQuery + tQuery + minQuery + maxQuery + pQuery
            }
            if (section === "material/predicted" || section === "tablebase/predicted") {
                setUrl2(url2)
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
                    </div> : <> 
                        {section === "material/predicted" || section === "tablebase/predicted" ? 
                        <div>
                            <EndgamesPredictedWDLCharts name={name} url={url} generalUrl={url2} />
                        </div> :
                        <div>
                            <EndgamesCharts name={name} url={url} />
                        </div>
                        }
                    </>
                    }
                </> :
                <div>
                    <EndgamesGeneralCharts name={name} url={url} />
                </div>
                }
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); setSection(""); setPieces(""); setUrl2(""); e.preventDefault();}}>Back</button>
                </div>
            </div>
        )
    }
    else {
        return (
            <div className="bg-light">
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
                            <option value="tablebase">Tablebase</option>
                            <option value="tablebase/predicted">Tablebase Predicted WDL</option>
                        </select>
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="opponent" style={{float: "left"}}>Only use matches against this opponent:</label>
                        <input id="opponent" className="form-control" placeholder="Enter opponent name" type="text" onChange={(e) => setOpponent(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="minelo" style={{float: "left"}}>Min Elo:</label>
                        <input id="minelo" className="form-control" placeholder="Enter minimum elo" type="number" onChange={(e) => setMinElo(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="maxelo" style={{float: "left"}}>Max Elo:</label>
                        <input id="maxelo" className="form-control" placeholder="Enter maximum elo" type="number" onChange={(e) => setMaxElo(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="datefrom" style={{float: "left"}}>Only use matches played after this date:</label>
                        <input id="datefrom" className="form-control" placeholder="Enter from date" type="date" onChange={(e) => setFrom(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="dateto" style={{float: "left"}}>Only use matches played before this date:</label>
                        <input id="dateto" className="form-control" placeholder="Enter to date" type="date" onChange={(e) => setTo(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="pieces" style={{float: "left"}}>How many pieces must be left on the board to be considered an endgame:</label>
                        <input id="pieces" className="form-control" placeholder="Enter number of pieces" type="number" onChange={(e) => setPieces(e.target.value)} />
                    </div>
                    <br/>
                    <input type="submit" value="Submit" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}

export default Endgames;