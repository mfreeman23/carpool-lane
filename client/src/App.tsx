import './App.css';
import { useState } from 'react';

function App() {

  const baseURL = "http://localhost:8080";

  type Step = "vehicle_search" | "vehicle_select" | "trip_form" | "results";
  type Car = {
    name: string;
    id: number;
  }
  const [currentStep, setCurrentStep] = useState<Step>("vehicle_search");
  const [vehicleOptions, setVehicleOptions] = useState<Car[]>([]);

  async function handleVehicleSearch(){

    // hide first form
    const url = baseURL + "/find_vehicle";
    
    // submit user entered data to backend find_vehicle function
    const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify({ username: "example" }),
    });

    // show returned vehicle options
    setCurrentStep("vehicle_select")

  }

  function handleVehicleSelection(){

    // save the id of the selected vehicle (the id RETURNED by the backend)

    // hide these selection options

    // display the second form for trip info collection
    setCurrentStep("trip_form")

  }

  async function handleTripSubmission(){

    setCurrentStep("results");

    // send trip info (including prev. selected vehicle id) to calculate_trip backend function
     const url = baseURL + "/calculate_trip";
     const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify({ username: "example" }),
    });

    // hide this form and display the calculated total price and per passenger prices

  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Carpool Lane</h1>

      </header>
    </div>
  );
}

export default App;
