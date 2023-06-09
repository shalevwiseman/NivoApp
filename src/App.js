import { useRef, useState } from 'react';
import React from 'react';
import './App.css';
import { v4 as uuidv4 } from 'uuid';
import Datepicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

function App() {

  
  const [date, setDate] = useState(new Date());
  const [startDate, setStartDate] = useState()
  const [endDate, setEndDate] = useState()



  const handleTimeChange = (dateInterval) => {
    const [start, end] = dateInterval;
    setStartDate(start);
    setEndDate(end);
  };

  return (
    <div className="App">
      <h1>Nivo App</h1>
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
    </div>
  );
}

export default App;
