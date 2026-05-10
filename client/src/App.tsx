import './App.css';
import { useState } from 'react';

function App() {

  type Step = "vehicle_search" | "vehicle_select" | "trip_form" | "results";
  const [currentStep, setCurrentStep] = useState<Step>("vehicle_search");

  

  function handleFirstForm(){

    // hide first form
    
    // submit user entered data to backend find_vehicle function

    // show returned vehicle options

    setCurrentStep("vehicle_select")


  }

  function handleVehicleSelection(){

    // save the id of the selected vehicle (the id RETURNED by the backend)

    // hide these selection options

    // display the second form for trip info collection
    setCurrentStep("trip_form")

  }

  function handleTripSubmission(){

    setCurrentStep("results")

    // send trip info (including prev. selected vehicle id) to calculate_trip backend function

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
