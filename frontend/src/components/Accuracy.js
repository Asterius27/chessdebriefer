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
            <div>
                <div>
                    <AccuracyResponse name={name} url={url} />
                </div>
                <div style={{paddingBottom: "2%"}}>
                    <button onClick={(e) => {setUrl(""); setName(""); e.preventDefault();}}>Back</button>
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
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }

}

export default Accuracy;