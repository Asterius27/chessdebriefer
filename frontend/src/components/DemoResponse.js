import { useEffect, useState } from "react";
import LoadingSpinner from "./LoadingSpinner";

function DemoResponse({ name, url, onLoad }) {

    useEffect(() => {
        const fetchPercentages = async () => {
            const res = await fetch(url).catch(err => {alert("An error has occured, please go back and try again")})
            const data = await res.json()
            setData({ data: data })
        }
        fetchPercentages()
    }, []);
    
    const [data, setData] = useState({})

    if (Object.keys(data).length !== 0) {
        if (onLoad) {
            onLoad(true, url);
        }
        return (
            <div style={{margin: "auto", display: "table"}} className="div2PDF">
                <div style={{display: "table-row"}}>
                    <div style={{paddingRight: "50px", display: "table-cell"}}>
                        <h3>Your Best</h3>
                        <ol>
                            {data["data"]["your best"].map(function(elem){
                                return (
                                    <li key={elem}>{elem}</li>
                                )
                            })}
                        </ol>
                    </div>
                    <div style={{display: "table-cell"}}>
                        <h3>Other Players Best</h3>
                        <ol>
                            {data["data"]["other players best"].map(function(elem){
                                return (
                                    <li key={elem}>{elem}</li>
                                )
                            })}
                        </ol>
                    </div>
                </div>
                <div style={{display: "table-row"}}>
                    <div style={{paddingRight: "50px", display: "table-cell"}}>
                        <h3>Your Worst</h3>
                        <ol>
                            {data["data"]["your worst"].map(function(elem){
                                return (
                                    <li key={elem}>{elem}</li>
                                )
                            })}
                        </ol>
                    </div>
                    <div style={{display: "table-cell"}}>
                        <h3>Other Players Worst</h3>
                        <ol>
                            {data["data"]["other players worst"].map(function(elem){
                                return (
                                    <li key={elem}>{elem}</li>
                                )
                            })}
                        </ol>
                    </div>
                </div>
            </div>
        )
    }  else {
        return (
            <LoadingSpinner />
        )
    }
}

export default DemoResponse;
