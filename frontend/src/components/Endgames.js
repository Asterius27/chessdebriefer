import { useState } from "react";
import PlayersGeneralCharts from "./PlayersGeneralCharts";
import PlayersCharts from "./PlayersCharts";
import PlayersOpeningCharts from "./PlayersOpeningCharts";

// TODO check date format
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
    
    // TODO
    const submitForm = (e) => {
        let oQuery = "", fQuery = "", tQuery = "", minQuery = "", maxQuery = "", eQuery = ""
        if (name) {
            let url = "http://localhost:8000/" + name + "/percentages"
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
            if (eco) {
                eQuery = "eco=" + eco + "&"
            }
            if (oQuery || fQuery || tQuery || minQuery || maxQuery || eQuery ) {
                url = url + "?" + oQuery + fQuery + tQuery + minQuery + maxQuery + eQuery
            }
            setUrl(url)
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div>
                {section ? <>
                    {section === "openings" && eco ? 
                    <div>
                        <PlayersOpeningCharts name={name} url={url} />
                    </div> :
                    <div>
                        <PlayersCharts name={name} url={url} />
                    </div>
                    }
                </> :
                <div>
                    <PlayersGeneralCharts name={name} url={url} />
                </div>
                }
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); setSection(""); setEco(""); e.preventDefault();}}>Back</button>
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
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }
}

export default Endgames;