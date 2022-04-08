import { useState } from "react";
import ThrowsComebacksCharts from "./ThrowsComebacksCharts";

function ThrowsComebacks() {

    const [opponent, setOpponent] = useState("")
    const [from, setFrom] = useState("")
    const [to, setTo] = useState("")
    const [minElo, setMinElo] = useState("")
    const [maxElo, setMaxElo] = useState("")
    const [name, setName] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let oQuery = "", fQuery = "", tQuery = "", minQuery = "", maxQuery = ""
        if (name) {
            let url = "http://localhost:8000/" + name + "/percentages/throws-comebacks"
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
            if (oQuery || fQuery || tQuery || minQuery || maxQuery ) {
                url = url + "?" + oQuery + fQuery + tQuery + minQuery + maxQuery
            }
            setUrl(url)
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div>
                <div>
                    <ThrowsComebacksCharts name={name} url={url} />
                </div>
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); e.preventDefault();}}>Back</button>
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
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }
}

export default ThrowsComebacks;