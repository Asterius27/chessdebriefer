import { useState } from "react";
import AccuracyResponse from "./AccuracyResponse";

function Accuracy() {

    const [name, setName] = useState("")
    const [url, setUrl] = useState("")

    const submitForm = (e) => {
        if (name) {
            setUrl("http://localhost:8000/" + name + "/accuracy")
        }
        e.preventDefault()
    }

    if (url) {
        return (
            <div className="bg-light">
                <div>
                    <AccuracyResponse name={name} url={url} />
                </div>
                <div style={{paddingBottom: "2%"}}>
                    <button className="btn btn-primary" onClick={(e) => {setUrl(""); setName(""); e.preventDefault();}}>Back</button>
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
                    <input type="submit" value="Submit" className="btn btn-primary" />
                </form>
            </div>
        )
    }

}

export default Accuracy;