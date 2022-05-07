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
            let url = process.env.REACT_APP_BACKEND_URL + name + "/percentages/throws-comebacks"
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
            <div className="bg-light">
                <div>
                    <ThrowsComebacksCharts name={name} url={url} />
                </div>
                <div style={{paddingBottom: "2%"}}>
                    <button className="btn btn-primary" onClick={(e) => {setUrl(""); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); e.preventDefault();}}>Back</button>
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
                    <input type="submit" value="Submit" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}

export default ThrowsComebacks;