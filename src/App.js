import { useRef, useState } from 'react';
import React from 'react';
import './App.css';
import { v4 as uuidv4 } from 'uuid';
import Datepicker from 'react-datepicker';
import { Grid } from '@material-ui/core';
import 'react-datepicker/dist/react-datepicker.css';
import intervalList from './intervalList';
import moment from 'moment';
import {
  Button,
  Container,
  List,
  ListItem,
  ListItemText,
  TextField,
  Typography,
  ToggleButtonGroup,
  ToggleButton,
  Divider,
} from "@mui/material";
function App() {

  
  const [startDate, setStartDate] = useState()
  const [endDate, setEndDate] = useState()
  const [intervals, setIntervals] = useState([{id: uuidv4(), name: "", start: "start", end: "end", sumMinutes: "sumMinutes"}])
  const [newTitle, setNewTitle] = useState('')

  const handleSubmit = (e, name, start, end) => {
    e.preventDefault()
    
    const startDate = moment(start)
    const endDate = moment(end)
    const sumMinutes = endDate.diff(startDate, 'minutes')
    // add new interval to intervals
    setIntervals([...intervals, {id: uuidv4(), name: name, start: start, end: end, sumMinutes: sumMinutes}])
    
  }





  return (
    <div className="App">
      <Container>
      <h1>Nivo App</h1>
      <Grid container spacing={3}>
      <intervalList intervals={intervals} />
      <Datepicker
      showTimeSelect
      timeFormat="HH:mm"
      timeIntervals={1}
      timeCaption="time"
      dateFormat="dd/MM/yyy, HH:mm"
      selectsStart
      selected={startDate}
      onChange={date => setStartDate(date)}
      startDate={startDate}  
      />
      <Datepicker
      showTimeSelect
      timeFormat="HH:mm"
      timeIntervals={1}
      timeCaption="time"
      dateFormat="dd/MM/yyy, HH:mm"
      selectsEnd
      selected={endDate}
      onChange={date => setEndDate(date)}
      endDate={endDate}
      minDate={startDate}
      />
      <TextField
          label="Title"
          fullWidth
          margin="normal"
          onChange={(event) => {
            setNewTitle(event.target.value);
          }}
          data-testid={`todoList-addTodo-title`}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={(e) => handleSubmit(e, newTitle, startDate, endDate)}
          data-testid={`todoList-addTodo-submitBtn`}
        >
          Submit
        </Button>
      
      </Grid>
      
      </Container>
    </div>
  );
}

export default App;
