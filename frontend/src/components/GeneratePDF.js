import { useState } from "react";
import PlayersGeneralCharts from "./PlayersGeneralCharts";
import PlayersCharts from "./PlayersCharts";
import PlayersOpeningCharts from "./PlayersOpeningCharts";
import ComparesCharts from "./ComparesCharts";
import ComparesGeneralCharts from "./ComparesGeneralCharts";
import EndgamesCharts from "./EndgamesCharts";
import EndgamesGeneralCharts from "./EndgamesGeneralCharts";
import EndgamesWDLCharts from "./EndgamesWDLCharts";
import EndgamesPredictedWDLCharts from "./EndgamesPredictedWDLCharts";
import EndgamesCompareGeneralCharts from "./EndgamesCompareGeneralCharts";
import EndgamesCompareCharts from "./EndgamesCompareCharts";
import EndgamesCompareWDLCharts from "./EndgamesCompareWDLCharts";
import EndgamesComparePredictedWDLCharts from "./EndgamesComparePredictedWDLCharts";
import ThrowsComebacksCharts from "./ThrowsComebacksCharts";
import LoadingSpinner from './LoadingSpinner';
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
                percentages_endgames_tablebase_predicted_compare: url + "/percentages/endgames/tablebase/predicted/compare"
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
                for (let url in urls) {
                    urls[url] = urls[url] + "?" + oQuery + fQuery + tQuery + minQuery + maxQuery + eQuery + eloQuery + rQuery + eventQuery + terminationQuery + limitQuery + minPlayedQuery + piecesQuery
                }
            }
            setUrls(urls)
        }
        e.preventDefault()
    }

    let loaded = {}
    let generate = true;
    const load = (state, origin) => {
        if (state) {
            loaded[origin] = true;
            if (Object.keys(loaded).length === 21 && generate) {
                generate = false;
                setTimeout(generatePDF, 2000);
            }
        }
    }

    const generatePDF = async () => {
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
        doc.save('report.pdf');
        document.getElementById("backbutton").click();
    }

    if (urls && Object.keys(urls).length !== 0) {
        return (
            <div className="bg-light">
                <div style={{overflow: "hidden", height: "0"}}>
                    <div>
                        <PlayersGeneralCharts name={name} url={urls["percentages"]} onLoad={load} />
                    </div>
                    <div>
                        <PlayersCharts name={name} url={urls["percentages_events"]} onLoad={load} section={"events"} />
                    </div>
                    <div>
                        <PlayersCharts name={name} url={urls["percentages_terminations"]} onLoad={load} section={"terminations"} />
                    </div>
                    {eco ? 
                    <div>
                        <PlayersOpeningCharts name={name} url={urls["percentages_openings"]} onLoad={load} />
                    </div> :
                    <div>
                        <PlayersCharts name={name} url={urls["percentages_openings"]} onLoad={load} section={"openings"} />
                    </div>
                    }
                    <div>
                        <ComparesGeneralCharts name={name} url={urls["percentages_compare"]} onLoad={load} />
                    </div>
                    <div>
                        <ComparesCharts name={name} url={urls["percentages_events_compare"]} onLoad={load} />
                    </div>
                    <div>
                        <ComparesCharts name={name} url={urls["percentages_terminations_compare"]} onLoad={load} />
                    </div>
                    <div>
                        <ComparesCharts name={name} url={urls["percentages_openings_compare"]} onLoad={load} />
                    </div>
                    <div>
                        <EndgamesGeneralCharts name={name} url={urls["percentages_endgames"]} onLoad={load} />
                    </div>
                    <div>
                        <EndgamesCharts name={name} url={urls["percentages_endgames_material"]} onLoad={load} section={"material"} />
                    </div>
                    <div>
                        <EndgamesCharts name={name} url={urls["percentages_endgames_tablebase"]} onLoad={load} section={"tablebase"} />
                    </div>
                    <div>
                        <EndgamesWDLCharts name={name} url={urls["percentages_endgames_material_wdl"]} onLoad={load} />
                    </div>
                    <div>
                        <EndgamesPredictedWDLCharts name={name} url={urls["percentages_endgames_material_predicted"]} generalUrl={urls["percentages_endgames"]} onLoad={load} section={"material"} />
                    </div>
                    <div>
                        <EndgamesPredictedWDLCharts name={name} url={urls["percentages_endgames_tablebase_predicted"]} generalUrl={urls["percentages_endgames"]} onLoad={load} section={"tablebase"} />
                    </div>
                    <div>
                        <EndgamesCompareGeneralCharts name={name} url={urls["percentages_endgames_compare"]} onLoad={load} />
                    </div>
                    <div>
                        <EndgamesCompareCharts name={name} url={urls["percentages_endgames_material_compare"]} onLoad={load} section={"material"} />
                    </div>
                    <div>
                        <EndgamesCompareCharts name={name} url={urls["percentages_endgames_tablebase_compare"]} onLoad={load} section={"tablebase"} />
                    </div>
                    <div>
                        <EndgamesCompareWDLCharts name={name} url={urls["percentages_endgames_material_wdl_compare"]} onLoad={load} />
                    </div>
                    <div>
                        <EndgamesComparePredictedWDLCharts name={name} url={urls["percentages_endgames_material_predicted_compare"]} onLoad={load} section={"material"} />
                    </div>
                    <div>
                        <EndgamesComparePredictedWDLCharts name={name} url={urls["percentages_endgames_tablebase_predicted_compare"]} onLoad={load} section={"tablebase"} />
                    </div>
                    <div>
                        <ThrowsComebacksCharts name={name} url={urls["percentages_throws_comebacks"]} onLoad={load} />
                    </div>
                </div>
                <LoadingSpinner />
                <div style={{paddingBottom: "2%"}}>
                    <button id="backbutton" className="btn btn-primary" onClick={(e) => {loaded = {}; generate = true; setUrls({}); setName(""); setMaxElo(""); setMinElo(""); setTo(""); setFrom(""); setOpponent(""); setEco(""); setElo(""); setRange(""); setEvent(""); setTermination(""); setLimit(""); setMinPlayed(""); setPieces(""); e.preventDefault();}}>Back</button>
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
                        <label htmlFor="events" style={{float: "left"}}>Event(s):</label>
                        <input id="events" className="form-control" placeholder="Enter event(s)" type="text" onChange={(e) => setEvent(e.target.value)}/>
                        <br/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="terminations" style={{float: "left"}}>Termination(s):</label>
                        <input id="terminations" className="form-control" placeholder="Enter termination(s)" type="text" onChange={(e) => setTermination(e.target.value)}/>
                        <br/>
                    </div>
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
                    <div className="form-group">
                        <label htmlFor="pieces" style={{float: "left"}}>How many pieces must be left on the board to be considered an endgame:</label>
                        <input id="pieces" className="form-control" placeholder="Enter number of pieces" type="number" onChange={(e) => setPieces(e.target.value)} />
                    </div>
                    <br/>
                    <input type="submit" value="Generate PDF Report" className="btn btn-primary" />
                </form>
            </div>
        )
    }
}

export default GeneratePDF;
