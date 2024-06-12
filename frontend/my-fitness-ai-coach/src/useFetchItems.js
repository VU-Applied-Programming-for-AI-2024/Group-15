import { useState, useEffect } from 'react';

// Use the correct backend URL
const API_URL = process.env.REACT_APP_API_URL || 'http://myfitnessaicoach-backend.azurewebsites.net';

const useFetchItems = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await fetch(`${API_URL}/api/items`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setItems(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchItems();
  }, []);

  const addItem = async (newItem) => {
    try {
      const response = await fetch(`${API_URL}/api/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newItem),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const item = await response.json();
      setItems((prevItems) => [...prevItems, item]);
    } catch (error) {
      setError(error);
    }
  };

  return { items, loading, error, addItem };
};

export default useFetchItems;
