"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [datasetType, setDatasetType] = useState('google'); // Default dataset is google

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
              {data.slice(0, 50).map((row, index) => (
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
