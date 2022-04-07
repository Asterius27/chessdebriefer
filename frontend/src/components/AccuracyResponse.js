import { useEffect, useState } from 'react';

function AccuracyResponse({ name, url }) {

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
        <div>
            <p>General accuracy: {data["data"]["general accuracy"]}</p>
            <p>Accuracy after the opening: {data["data"]["accuracy after opening"]}</p>
        </div>
    )

  }
    
}

export default AccuracyResponse;
