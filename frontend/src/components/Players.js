import { useState } from "react";
import PlayersGeneralCharts from "./PlayersGeneralCharts";
import PlayersCharts from "./PlayersCharts";
import PlayersOpeningCharts from "./PlayersOpeningCharts";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

function Players() {

    const [opponent, setOpponent] = useState("")
    const [from, setFrom] = useState("")
    const [to, setTo] = useState("")
    const [minElo, setMinElo] = useState("")
    const [maxElo, setMaxElo] = useState("")
    const [eco, setEco] = useState("")
    const [name, setName] = useState("")
    const [section, setSection] = useState("")
    const [url, setUrl] = useState("")
    
    const submitForm = (e) => {
        let oQuery = "", fQuery = "", tQuery = "", minQuery = "", maxQuery = "", eQuery = ""
        if (name) {
            let url = process.env.REACT_APP_BACKEND_URL + name + "/percentages"
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

    const generatePDF = (e) => {
        let charts = document.querySelectorAll(".div2PDF");
        const doc = new jsPDF("p", "pt", "a4");
        [...charts].forEach(function(chart) {
            let input_ratio = (chart.clientHeight * 1.0) / chart.clientWidth;
            html2canvas(chart, {
                allowTaint: true,
                useCORS: true
            }).then(canvas => { 
                var imgData = canvas.toDataURL('image/png');
                doc.addImage(
                    imgData, 
                    'png', 
                    1,
                    1,
                    590,
                    input_ratio * 590
                );
                doc.addPage("a4", "p");
            });
        });
        doc.save('charts.pdf');
    } 

    if (url) {
        return (
            <div className="bg-light">
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
                    <button className="btn btn-primary" onClick={generatePDF}>Download PDF</button>
                </div>
                <div style={{paddingBottom: "2%"}}>
                    <button className="btn btn-primary" onClick={(e) => {setUrl(""); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); setSection(""); setEco(""); e.preventDefault();}}>Back</button>
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
                    {section === "openings" ? 
                    <div className="form-group">
                        <label htmlFor="ecos" style={{float: "left"}}>Eco(s):</label>
                        <input id="ecos" className="form-control" placeholder="Enter eco(s)" type="text" onChange={(e) => setEco(e.target.value)}/>
                        <br/>
                    </div> : <div></div>
                    }
                    <input type="submit" value="Submit" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}

export default Players;