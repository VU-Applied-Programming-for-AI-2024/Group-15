import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);
  const [postData, setPostData] = useState({ message: '' });
  const [response, setResponse] = useState(null);

  useEffect(() => {
    // Fetch data from Flask backend
    axios.get('http://localhost:5000/api/data')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  const handlePost = () => {
    // Post data to Flask backend
    axios.post('http://localhost:5000/api/data', postData)
      .then(response => {
        setResponse(response.data);
      })
      .catch(error => {
        console.error('There was an error posting the data!', error);
      });
  };

  return (
    <div className="App">
      <h1>Data from Flask</h1>
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : 'Loading...'}
      
      <h2>Send Data to Flask</h2>
      <input 
        type="text" 
        value={postData.message}
        onChange={(e) => setPostData({ message: e.target.value })}
      />
      <button onClick={handlePost}>Send</button>
      
      <h2>Response from Flask</h2>
      {response ? <pre>{JSON.stringify(response, null, 2)}</pre> : 'No response yet.'}
    </div>
  );
}

export default App;
