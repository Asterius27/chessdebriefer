import { useState } from "react";
import PlayersGeneralCharts from "./PlayersGeneralCharts";
import PlayersCharts from "./PlayersCharts";
import PlayersOpeningCharts from "./PlayersOpeningCharts";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

function GeneratePDF() {

    const [opponent, setOpponent] = useState("")
    const [from, setFrom] = useState("")
    const [to, setTo] = useState("")
    const [minElo, setMinElo] = useState("")
    const [maxElo, setMaxElo] = useState("")
    const [elo, setElo] = useState("")
    const [range, setRange] = useState("")
    const [event, setEvent] = useState("")
    const [termination, setTermination] = useState("")
    const [limit, setLimit] = useState("")
    const [minPlayed, setMinPlayed] = useState("")
    const [pieces, setPieces] = useState("")
    const [eco, setEco] = useState("")
    const [name, setName] = useState("")
    const [urls, setUrls] = useState({})

    const submitForm = (e) => {
        let oQuery = "", fQuery = "", tQuery = "", minQuery = "", maxQuery = "", eQuery = "", eloQuery = "", rQuery = "", eventQuery = "", terminationQuery = "", limitQuery = "", minPlayedQuery = "", piecesQuery = ""
        if (name) {
            let url = process.env.REACT_APP_BACKEND_URL + name
            let urls = {
                percentages: url + "/percentages",
                percentages_compare: url + "/percentages/compare",
                percentages_events: url + "/percentages/events",
                percentages_events_compare: url + "/percentages/events/compare",
                percentages_openings: url + "/percentages/openings",
                percentages_openings_compare: url + "/percentages/openings/compare",
                percentages_demo: url + "/percentages/openings/best-worst",
                percentages_terminations: url + "/percentages/terminations",
                percentages_terminations_compare: url + "/percentages/terminations/compare",
                percentages_throws_comebacks: url + "/percentages/throws-comebacks",
                percentages_endgames: url + "/percentages/endgames",
                percentages_endgames_compare: url + "/percentages/endgames/compare",
                percentages_endgames_material: url + "/percentages/endgames/material",
                percentages_endgames_material_compare: url + "/percentages/endgames/material/compare",
                percentages_endgames_material_wdl: url + "/percentages/endgames/material/wdl",
                percentages_endgames_material_wdl_compare: url + "/percentages/endgames/material/wdl/compare",
                percentages_endgames_material_predicted: url + "/percentages/endgames/material/predicted",
                percentages_endgames_material_predicted_compare: url + "/percentages/endgames/material/predicted/compare",
                percentages_endgames_tablebase: url + "/percentages/endgames/tablebase",
                percentages_endgames_tablebase_compare: url + "/percentages/endgames/tablebase/compare",
                percentages_endgames_tablebase_predicted: url + "/percentages/endgames/tablebase/predicted",
                percentages_endgames_tablebase_predicted_compare: url + "/percentages/endgames/tablebase/predicted/compare",
                accuracy: url + "/accuracy"
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
            if (elo) {
                eloQuery = "elo=" + elo + "&"
            }
            if (range) {
                rQuery = "range=" + range + "&"
            }
            if (event) {
                eventQuery = "event=" + event + "&"
            }
            if (termination) {
                terminationQuery = "termination=" + termination + "&"
            }
            if (limit) {
                limitQuery = "limit=" + limit + "&"
            }
            if (minPlayed) {
                minPlayedQuery = "min_played=" + minPlayed + "&"
            }
            if (pieces) {
                piecesQuery = "pieces=" + pieces + "&"
            }
            if (oQuery || fQuery || tQuery || minQuery || maxQuery || eQuery || eloQuery || rQuery || eventQuery || terminationQuery || limitQuery || minPlayedQuery || piecesQuery) {
                for (let url of urls) {
                    urls[url] = urls[url] + "?" + oQuery + fQuery + tQuery + minQuery + maxQuery + eQuery + eloQuery + rQuery + eventQuery + terminationQuery + limitQuery + minPlayedQuery + piecesQuery
                }
            }
            setUrls(urls)
        }
        e.preventDefault()
    }

    const generatePDF = async (e) => {
        let charts = document.querySelectorAll(".div2PDF");
        const doc = new jsPDF("p", "pt", "a4");
        for (let i = 0; i < charts.length; i++) {
            let input_ratio = (charts[i].clientHeight * 1.0) / charts[i].clientWidth;
            let canvas = await html2canvas(charts[i], {
                allowTaint: true,
                useCORS: true
            });
            var imgData = canvas.toDataURL('image/png');
            doc.addImage(
                imgData, 
                'png', 
                1,
                1,
                590,
                input_ratio * 590,
                "chart" + i
            );
            if (i !== charts.length - 1) {
                doc.addPage("a4", "p");
            }
        }
        doc.save('charts.pdf');
    }

    if (urls && Object.keys(urls).length !== 0) {
        return (
            <div className="bg-light">
                <div>
                    <PlayersGeneralCharts name={name} url={urls["percentages"]} />
                </div>
                <div>
                    <PlayersCharts name={name} url={urls["percentages_events"]} />
                </div>
                <div>
                    <PlayersCharts name={name} url={urls["percentages_terminations"]} />
                </div>
                {eco ? 
                <div>
                    <PlayersOpeningCharts name={name} url={urls["percentages_openings"]} />
                </div> :
                <div>
                    <PlayersCharts name={name} url={urls["percentages_openings"]} />
                </div>
                }
                <div style={{paddingBottom: "2%"}}>
                    <button className="btn btn-primary" onClick={(e) => {setUrls({}); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); setEco(""); e.preventDefault();}}>Back</button>
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
                    <div className="form-group">
                        <label htmlFor="ecos" style={{float: "left"}}>Eco(s):</label>
                        <input id="ecos" className="form-control" placeholder="Enter eco(s)" type="text" onChange={(e) => setEco(e.target.value)}/>
                        <br/>
                    </div>
                    <input type="submit" value="Submit" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}

export default GeneratePDF;
