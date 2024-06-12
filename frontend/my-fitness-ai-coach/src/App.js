import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState({ id: '', name: '' });
  const [response, setResponse] = useState(null);

  useEffect(() => {
    // Fetch items from Flask backend
    axios.get('http://localhost:5000/api/items')
      .then(response => {
        setItems(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the items!', error);
      });
  }, []);

  const handleAddItem = () => {
    // Add new item to Flask backend
    axios.post('http://localhost:5000/api/items', newItem)
      .then(response => {
        setItems([...items, response.data]);
        setResponse(response.data);
        setNewItem({ id: '', name: '' });
      })
      .catch(error => {
        console.error('There was an error adding the item!', error);
      });
  };

  return (
    <div className="App">
      <h1>Data from Flask</h1>
      {items.length ? (
        <ul>
          {items.map(item => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      ) : (
        'Loading...'
      )}
      
      <h2>Send Data to Flask</h2>
      <input 
        type="text" 
        placeholder="ID"
        value={newItem.id}
        onChange={(e) => setNewItem({ ...newItem, id: e.target.value })}
      />
      <input 
        type="text" 
        placeholder="Name"
        value={newItem.name}
        onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
      />
      <button onClick={handleAddItem}>Send</button>
      
      <h2>Response from Flask</h2>
      {response ? <pre>{JSON.stringify(response, null, 2)}</pre> : 'No response yet.'}
    </div>
  );
}

export default App;
