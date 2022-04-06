import { useState } from "react";
import OpeningsChart from "./OpeningsChart";

function Openings() {

    const [tournament, setTournament] = useState("")
    const [minElo, setMinElo] = useState("")
    const [elo, setElo] = useState("")
    const [range, setRange] = useState("")
    const [eco, setEco] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let tQuery = "", meQuery = "", eQuery = "", rQuery = ""
        if (eco) {
            let url = "http://localhost:8000/" + eco + "/stats"
            if (tournament) {
                tQuery = "tournament=true&"
            }
            if (minElo) {
                meQuery = "min_elo=" + minElo + "&"
            }
            if (elo) {
                eQuery = "elo=" + elo + "&"
            }
            if (range) {
                rQuery = "range=" + range + "&"
            }
            if (tQuery || meQuery || eQuery || rQuery ) {
                url = url + "?" + tQuery + meQuery + eQuery + rQuery
            }
            setUrl(url)
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div>
                <div>
                    <OpeningsChart eco={eco} url={url} />
                </div>
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setEco(""); setRange(""); setElo(""); setMinElo(""); setTournament(""); e.preventDefault();}}>Back</button>
                </div>
            </div>
        )
    }
    else {
        return (
            <div>
                <form onSubmit={submitForm}>
                    <label>
                        Eco(s):
                        <input 
                            style={{marginLeft: "7px"}}
                            type="text"
                            onChange={(e) => setEco(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Only use tournament matches:
                        <div style={{marginLeft: "7px"}}>
                            <label>
                                <input type="radio" value="Yes" checked={tournament === "Yes"} onChange={(e) => setTournament(e.target.value)}/>
                                Yes
                            </label>
                        </div>
                        <div style={{marginLeft: "7px"}}>
                            <label>
                                <input type="radio" value="" checked={tournament === ""} onChange={(e) => setTournament(e.target.value)}/>
                                No
                            </label>
                        </div>
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
                        Elo:
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

export default Openings;