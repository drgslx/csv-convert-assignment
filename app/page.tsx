"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [datasetType, setDatasetType] = useState('google'); // Default dataset is google

  useEffect(() => {
    async function fetchData() {
      console.log("Selected dataset:", datasetType); 
      setLoading(true); // Set loading to true before fetching data
      try {
        const response = await fetch(`/api/csv-convert?dataset=${datasetType}`); // Pass dataset type as query parameter
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false); // Set loading to false after data is fetched or an error occurs
      }
    }

    fetchData();
  }, [datasetType]); // Re-run useEffect when datasetType changes

  // Extract headers from the data if it exists
  const headers = data.length > 0 ? Object.keys(data[0]) : [];

  return (
    <div className="mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">CSV Data:</h1>
      
      {/* Dropdown to select dataset */}
      <div className="mb-4">
        <label className="mr-4">Select Dataset:</label>
        <select 
          value={datasetType} 
          onChange={(e) => setDatasetType(e.target.value)} // Update dataset type on selection change
          className="border px-4 py-2"
        >
          <option value="google">Google Dataset</option>
          <option value="website">Website Dataset</option>
          <option value="facebook">Facebook Dataset</option>
        </select>
      </div>

      {loading ? (
        <p>Loading...</p> // Display loading message while fetching data
      ) : data.length > 0 ? (
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
          <tbody className="bg-white divide-y divide-gray-200 max-w-2xl">
            {data.slice(0, 25).map((row, index) => (
              <tr key={index}>
                {headers.map((header) => (
                  <td
                    key={header}
                    className="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                  >
                    <div className="px-6 max-w-[500px]">{row[header]}</div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No data available yet</p>
      )}
    </div>
  );
}
