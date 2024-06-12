import React from 'react';
import logo from './logo.svg';
import './App.css';
import useFetchItems from './useFetchItems';

function App() {
  const { items, loading, error, addItem } = useFetchItems();

  const handleAddItem = () => {
    const newItem = { name: 'New Item' };
    addItem(newItem);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Edit <code>src/App.js</code> and save to reload.</p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <div>
        <h1>Item List</h1>
        <ul>
          {items.map(item => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
        <button onClick={handleAddItem}>Add Item</button>
      </div>
    </div>
  );
}

export default App;
