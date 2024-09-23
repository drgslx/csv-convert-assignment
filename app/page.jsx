"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [datasetType, setDatasetType] = useState('google'); // Default dataset is google
  const [itemsToShow, setItemsToShow] = useState(50); // Default to show 50 items

  useEffect(() => {
    async function fetchData() {
      console.log("Selected dataset:", datasetType);
      setLoading(true);
      try {
        const response = await fetch(`/api/csv-convert?dataset=${datasetType}`);
        const result = await response.json();

        console.log("Fetched data:", result); // Log fetched data
        setData(result);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [datasetType]);

  // Fisher-Yates Shuffle Algorithm
  const shuffleArray = (array) => {
    const shuffledArray = [...array]; // Copy the array to avoid mutating the original array
    for (let i = shuffledArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
    }
    return shuffledArray;
  };

  // Shuffle the data and update it with only the number of items to show
  const shuffleData = () => {
    const shuffled = shuffleArray(data);
    setData(shuffled.slice(0, itemsToShow));
  };

  const headers = data.length > 0 ? Object.keys(data[0]) : [];

  return (
    <div className="mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">CSV Data:</h1>

      <div className="mb-4">
        <label className="mr-4">Select Dataset:</label>
        <select 
          value={datasetType} 
          onChange={(e) => setDatasetType(e.target.value)}
          className="border px-4 py-2"
        >
          <option value="google">Google Dataset</option>
          <option value="website">Website Dataset</option>
          <option value="website_address">Website Dataset with Address</option>
          <option value="facebook">Facebook Dataset</option>
          <option value="merged">Combined Dataset</option>
        </select>
      </div>

      <div className="mb-4">
        <button onClick={() => setItemsToShow(100)} className="mr-2 border px-4 py-2">Show 100</button>
        <button onClick={() => setItemsToShow(150)} className="mr-2 border px-4 py-2">Show 150</button>
        <button onClick={() => setItemsToShow(200)} className="border px-4 py-2">Show 200</button>
        <button onClick={() => setItemsToShow(300)} className="border px-4 py-2">Show 300</button>
        <button onClick={() => setItemsToShow(500)} className="border px-4 py-2">Show 500</button>
        <button onClick={shuffleData} className="ml-4 border px-4 py-2 bg-blue-500 text-white">Shuffle Data</button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : data.length > 0 ? (
        <div className="overflow-x-auto max-h-[720px] overflow-y-scroll">
          <table className="min-w-full divide-y divide-x divide-gray-200 border-collapse border border-gray-300">
            <thead className="bg-gray-200">
              <tr>
                {headers.map((header) => (
                  <th
                    key={header}
                    className="px-6 py-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-300"
                  >
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.slice(0, itemsToShow).map((row, index) => (
                <tr key={index}>
                  {headers.map((header) => (
                    <td
                      key={header}
                      className="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      <div className="">{row[header]}</div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>No data available yet</p>
      )}
    </div>
  );
}
