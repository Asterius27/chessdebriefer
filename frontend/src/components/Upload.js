import axios from "axios";
import { useState } from "react";

function Upload() {

    const [selectedFile, setSelectedFile] = useState("")
    const [url, setUrl] = useState(process.env.REACT_APP_BACKEND_URL + "upload")

    const submitForm = (e) => {
        const formData = new FormData();
        if (selectedFile && url) {
            formData.append("file", selectedFile)
            axios.post(url, formData)
                .then((res) => {
                    if (res.status === 200) {
                        alert(res.data)
                    }
                    else {
                        alert(res.status)
                    }
                })
                .catch((err) => alert("File upload failed"))
        }
        e.preventDefault()
    }

    const url1 = process.env.REACT_APP_BACKEND_URL + "upload"
    const url2 = process.env.REACT_APP_BACKEND_URL + "upload/openings"

    return (
        <div className="bg-light" style={{paddingBottom: "1%"}}>
            <form onSubmit={submitForm} style={{width: "80%", height: "80%", margin: "auto"}}>
                <br/>
                <div className="form-group">
                    <label htmlFor="choosesection" style={{float: "left"}}>Choose upload type:</label>
                    <select id="choosesection" className="form-select" value={url} onChange={(e) => setUrl(e.target.value)}>
                        <option value={url1}>Games</option>
                        <option value={url2}>Openings</option>
                    </select>
                </div>
                <br/>
                <div className="form-group">
                    <label htmlFor="pgn" style={{float: "left"}}>Select PGN file to upload:</label>
                    <input type="file" className="form-control-file" id="pgn" onChange={(e) => setSelectedFile(e.target.files[0])} />
                </div>
                <br/>
                <input type="submit" value="Submit" className="btn btn-primary" />
            </form>
        </div>
    )
}

export default Upload;