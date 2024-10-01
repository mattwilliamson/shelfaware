import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, Container } from 'react-bootstrap';  // Bootstrap components
import Button from '@mui/material/Button';  // Material UI Button

function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    // Fetch items from FastAPI backend
    axios.get('http://localhost:8000/items')
      .then(response => {
        setItems(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching the items!", error);
      });
  }, []);

  return (
    <Container>
      <h1 className="my-4">Item List</h1>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Quantity</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, index) => (
            <tr key={index}>
              <td>{item.name}</td>
              <td>{item.quantity}</td>
            </tr>
          ))}
        </tbody>
      </Table>

      <Button variant="contained" color="primary" onClick={() => alert("Add Item Clicked!")}>
        Add Item
      </Button>
    </Container>
  );
}

export default App;
