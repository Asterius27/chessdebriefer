import { useState } from "react";
import DemoResponse from "./DemoResponse";

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
            <div className="bg-light">
                <form onSubmit={submitForm} style={{width: "80%", height: "80%", margin: "auto"}}>
                <br/>
                    <div className="form-group">
                        <label htmlFor="playername" style={{float: "left"}}>Player Name:</label>
                        <input className="form-control" id="playername" placeholder="Enter player name" type="text" onChange={(e) => setName(e.target.value)} />
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
                        <label htmlFor="elo" style={{float: "left"}}>Elo to compare to:</label>
                        <input id="elo" className="form-control" placeholder="Enter elo" type="number" onChange={(e) => setElo(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="range" style={{float: "left"}}>Range:</label>
                        <input id="range" className="form-control" placeholder="Enter range" type="number" onChange={(e) => setRange(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="limit" style={{float: "left"}}>Limit response list to:</label>
                        <input id="limit" className="form-control" placeholder="Enter limit" type="number" onChange={(e) => setLimit(e.target.value)} />
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="minplayed" style={{float: "left"}}>Only consider openings that have at least this many matches played:</label>
                        <input id="minplayed" className="form-control" placeholder="Enter minimum played" type="number" onChange={(e) => setMinPlayed(e.target.value)} />
                    </div>
                    <br/>
                    <input type="submit" value="Submit" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}

export default Demo;