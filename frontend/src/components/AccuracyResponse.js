import { useEffect, useState } from 'react';
import LoadingSpinner from "./LoadingSpinner";

function AccuracyResponse({ name, url }) {

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

    return (
        <div style={{width: "80%", margin: "auto", paddingTop: "1%", paddingBottom: "1%"}}>
            <p>General accuracy: {data["data"]["general accuracy"]}</p>
            <p>Accuracy after the opening: {data["data"]["accuracy after opening"]}</p>
        </div>
    )

  } else {
    return (
      <LoadingSpinner />
    )
  }
    
}

export default AccuracyResponse;
