import { useState } from "react";
import ComparesCharts from "./ComparesCharts";
import ComparesGeneralCharts from "./ComparesGeneralCharts";

function Compares() {

    const [elo, setElo] = useState("")
    const [range, setRange] = useState("")
    const [event, setEvent] = useState("")
    const [eco, setEco] = useState("")
    const [termination, setTermination] = useState("")
    const [section, setSection] = useState("")
    const [name, setName] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let eloQuery = "", rQuery = "", eQuery = "", ecoQuery = "", tQuery = ""
        if (name) {
            let url = "http://localhost:8000/" + name + "/percentages"
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
            if (event) {
                eQuery = "event=" + event + "&"
            }
            if (eco) {
                ecoQuery = "eco=" + eco + "&"
            }
            if (termination) {
                tQuery = "termination=" + termination + "&"
            }
            if (eloQuery || rQuery || eQuery || ecoQuery || tQuery ) {
                url = url + "?" + eloQuery + rQuery + eQuery + ecoQuery + tQuery
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
                    <ComparesCharts name={name} url={url} />
                </div> :
                <div>
                    <ComparesGeneralCharts name={name} url={url} />
                </div>
                }
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setName(""); setElo(""); setRange(""); setEvent(""); setTermination(""); setSection(""); setEco(""); e.preventDefault();}}>Back</button>
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
                            <option value="events">Events</option>
                            <option value="openings">Openings</option>
                            <option value="terminations">Terminations</option>
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
                    {section === "openings" ? 
                    <label>
                        Eco(s):
                        <input 
                            style={{marginLeft: "7px"}}
                            type="text"
                            onChange={(e) => setEco(e.target.value)}
                        />
                        <br/>
                        <br/>
                    </label> : <div></div>
                    }
                    {section === "events" ? 
                    <label>
                        Event(s):
                        <input 
                            style={{marginLeft: "7px"}}
                            type="text"
                            onChange={(e) => setEvent(e.target.value)}
                        />
                        <br/>
                        <br/>
                    </label> : <div></div>
                    }
                    {section === "terminations" ? 
                    <label>
                        Termination(s):
                        <input 
                            style={{marginLeft: "7px"}}
                            type="text"
                            onChange={(e) => setTermination(e.target.value)}
                        />
                        <br/>
                        <br/>
                    </label> : <div></div>
                    }
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }
}

export default Compares;