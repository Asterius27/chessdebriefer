import { useState } from "react";
import DemoResponse from "./DemoResponse";

// TODO check date format
function Demo() {

    const [opponent, setOpponent] = useState("")
    const [from, setFrom] = useState("")
    const [to, setTo] = useState("")
    const [minElo, setMinElo] = useState("")
    const [maxElo, setMaxElo] = useState("")
    const [elo, setElo] = useState("")
    const [range, setRange] = useState("")
    const [limit, setLimit] = useState("")
    const [minPlayed, setMinPlayed] = useState("")
    const [name, setName] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let oQuery = "", fQuery = "", tQuery = "", minQuery = "", maxQuery = "", eQuery = "", rQuery = "", lQuery = "", mpQuery = ""
        if (name) {
            let url = "http://localhost:8000/" + name + "/percentages/openings/best-worst"
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
            if (elo) {
                eQuery = "elo=" + elo + "&"
            }
            if (range) {
                rQuery = "range=" + range + "&"
            }
            if (limit) {
                lQuery = "limit=" + limit + "&"
            }
            if (minPlayed) {
                mpQuery = "min_played=" + minPlayed + "&"
            }
            if (oQuery || fQuery || tQuery || minQuery || maxQuery || eQuery || rQuery || lQuery || mpQuery ) {
                url = url + "?" + oQuery + fQuery + tQuery + minQuery + maxQuery + eQuery + rQuery + lQuery + mpQuery
            }
            setUrl(url)
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div>
                <div>
                    <DemoResponse name={name} url={url} />
                </div>
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); setElo(""); setRange(""); setLimit(""); setMinPlayed(""); e.preventDefault();}}>Back</button>
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
                        Compare to players with this elo:
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
                    <label>
                        Limit response list to:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="number"
                            onChange={(e) => setLimit(e.target.value)}
                        />
                    </label>
                    <br/>
                    <br/>
                    <label>
                        Only consider openings that have at least this many matches played:
                        <input 
                            style={{marginLeft: "7px"}}
                            type="number"
                            onChange={(e) => setMinPlayed(e.target.value)}
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

export default Demo;