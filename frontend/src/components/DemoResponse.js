import { useEffect, useState } from "react";

function DemoResponse({ name, url }) {

    useEffect(() => {
        const fetchPercentages = async () => {
            const res = await fetch(url)
            const data = await res.json()
            setData({ data: data })
        }
        fetchPercentages()
    }, []);
    
    const [data, setData] = useState({})

    if (Object.keys(data).length !== 0) {
        return (
            <div style={{margin: "auto", display: "table"}}>
                <div style={{display: "table-row"}}>
                    <div style={{paddingRight: "50px", display: "table-cell"}}>
                        <h3>Your Best</h3>
                        <ol>
                            {data["data"]["your best"].map(function(elem){
                                return (
                                    <li>{elem}</li>
                                )
                            })}
                        </ol>
                    </div>
                    <div style={{display: "table-cell"}}>
                        <h3>Other Players Best</h3>
                        <ol>
                            {data["data"]["other players best"].map(function(elem){
                                return (
                                    <li>{elem}</li>
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
                                    <li>{elem}</li>
                                )
                            })}
                        </ol>
                    </div>
                    <div style={{display: "table-cell"}}>
                        <h3>Other Players Worst</h3>
                        <ol>
                            {data["data"]["other players worst"].map(function(elem){
                                return (
                                    <li>{elem}</li>
                                )
                            })}
                        </ol>
                    </div>
                </div>
            </div>
        )
    }
}

export default DemoResponse;