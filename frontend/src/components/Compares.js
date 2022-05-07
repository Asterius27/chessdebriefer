import { useState } from "react";
import ComparesCharts from "./ComparesCharts";
import ComparesGeneralCharts from "./ComparesGeneralCharts";

function Compares() {

    const [minElo, setMinElo] = useState("")
    const [maxElo, setMaxElo] = useState("")
    const [elo, setElo] = useState("")
    const [range, setRange] = useState("")
    const [event, setEvent] = useState("")
    const [eco, setEco] = useState("")
    const [termination, setTermination] = useState("")
    const [section, setSection] = useState("")
    const [name, setName] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let eloQuery = "", rQuery = "", eQuery = "", ecoQuery = "", tQuery = "", minQuery = "", maxQuery = ""
        if (name) {
            let url = process.env.REACT_APP_BACKEND_URL + name + "/percentages"
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
            if (event) {
                eQuery = "event=" + event + "&"
            }
            if (eco) {
                ecoQuery = "eco=" + eco + "&"
            }
            if (termination) {
                tQuery = "termination=" + termination + "&"
            }
            if (eloQuery || rQuery || eQuery || ecoQuery || tQuery || maxQuery || minQuery ) {
                url = url + "?" + minQuery + maxQuery + eloQuery + rQuery + eQuery + ecoQuery + tQuery
            }
            setUrl(url)
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div className="bg-light">
                {section ? 
                <div>
                    <ComparesCharts name={name} url={url} />
                </div> :
                <div>
                    <ComparesGeneralCharts name={name} url={url} />
                </div>
                }
                <div style={{paddingBottom: "2%"}}>
                    <button className="btn btn-primary" onClick={(e) => {setUrl(""); setName(""); setElo(""); setRange(""); setEvent(""); setTermination(""); setSection(""); setEco(""); setMaxElo(""); setMinElo(""); e.preventDefault();}}>Back</button>
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
                            <option value="events">Events</option>
                            <option value="openings">Openings</option>
                            <option value="terminations">Terminations</option>
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
                    {section === "openings" ? 
                    <div className="form-group">
                        <label htmlFor="ecos" style={{float: "left"}}>Eco(s):</label>
                        <input id="ecos" className="form-control" placeholder="Enter eco(s)" type="text" onChange={(e) => setEco(e.target.value)}/>
                        <br/>
                    </div> : <div></div>
                    }
                    {section === "events" ? 
                    <div className="form-group">
                        <label htmlFor="events" style={{float: "left"}}>Event(s):</label>
                        <input id="events" className="form-control" placeholder="Enter event(s)" type="text" onChange={(e) => setEvent(e.target.value)}/>
                        <br/>
                    </div> : <div></div>
                    }
                    {section === "terminations" ? 
                    <div className="form-group">
                        <label htmlFor="terminations" style={{float: "left"}}>Termination(s):</label>
                        <input id="terminations" className="form-control" placeholder="Enter termination(s)" type="text" onChange={(e) => setTermination(e.target.value)}/>
                        <br/>
                    </div> : <div></div>
                    }
                    <input type="submit" value="Submit" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}

export default Compares;