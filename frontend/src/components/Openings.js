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
            <div className="bg-light">
                <div>
                    <OpeningsChart eco={eco} url={url} />
                </div>
                <div style={{paddingBottom: "2%"}}>
                    <button className="btn btn-primary" onClick={(e) => {setUrl(""); setEco(""); setRange(""); setElo(""); setMinElo(""); setTournament(""); e.preventDefault();}}>Back</button>
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
                        <label htmlFor="ecos" style={{float: "left"}}>Eco(s):</label>
                        <input id="ecos" className="form-control" placeholder="Enter eco(s)" type="text" onChange={(e) => setEco(e.target.value)}/>
                    </div>
                    <br/>
                    <legend style={{textAlign: "left", fontSize: "16px"}}>Only use tournament matches:</legend>
                    <div className="form-check">
                        <input className="form-check-input" id="radioyes" type="radio" value="Yes" checked={tournament === "Yes"} onChange={(e) => setTournament(e.target.value)}/>
                        <label className="form-check-label" style={{float: "left"}} htmlFor="radioyes">Yes</label>
                    </div>
                    <div className="form-check">
                        <input className="form-check-input" id="radiono" type="radio" value="" checked={tournament === ""} onChange={(e) => setTournament(e.target.value)}/>
                        <label className="form-check-label" style={{float: "left"}} htmlFor="radiono">No</label>
                    </div>
                    <br/>
                    <div className="form-group">
                        <label htmlFor="minelo" style={{float: "left"}}>Min Elo:</label>
                        <input id="minelo" className="form-control" placeholder="Enter minimum elo" type="number" onChange={(e) => setMinElo(e.target.value)} />
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

export default Openings;