import axios from "axios";
import { useState } from "react";

// TODO check file type
function Upload() {

    const [selectedFile, setSelectedFile] = useState("")
    const [url, setUrl] = useState("http://localhost:8000/upload")

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
                .catch((err) => alert("Error"))
        }
        e.preventDefault()
    }

    return (
        <div>
            <form onSubmit={submitForm}>
                <label>
                    Choose upload type:
                    <select style={{marginLeft: "7px"}} value={url} onChange={(e) => setUrl(e.target.value)}>
                        <option value="http://localhost:8000/upload">Games</option>
                        <option value="http://localhost:8000/upload/openings">Openings</option>
                    </select>
                </label>
                <br/>
                <br/>
                <input 
                    type="file"
                    onChange={(e) => setSelectedFile(e.target.files[0])}
                />
                <br/>
                <br/>
                <input type="submit" value="Submit" />
            </form>
        </div>
    )
}

export default Upload;