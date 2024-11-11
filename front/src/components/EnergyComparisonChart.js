
import { useEffect, useState, useRef } from "react";
import getEnergyComparison from "../services/ApiService";
import Chart from 'chart.js/auto';
import axios from "axios";

const months = [1, 2, 3, 4, 5, 6, 7, 8, ,9, 10, 11, 12];

function EnergyComparisonChart() {
    const [energyComparison, setEnergyComparison] = useState();
    const canvasRef = useRef(null);

    useEffect(() => {
        // setEnergyComparison(getEnergyComparison());
        axios
        .get("http://127.0.0.1:8000/api/before_after_energy_usage/1e0e7511-9e40-4b13-8c52-4f9c26c41c55")
        .then(res => {
            const energyComparison = res.data;
            let baselineData = [];
            let improvedData = [];
            for(let key in energyComparison.baseline){
                baselineData.push(energyComparison.baseline[key].energy);
            }
            for(let key in energyComparison.baseline){
                improvedData.push(energyComparison.improved[key].energy);
            }
            console.log(baselineData)
            new Chart(canvasRef.current, 
                {
                    type: 'line', 
                    data: {labels: months, datasets: [
                        {label: "baseline", data: baselineData},
                        {label: "improved", data: improvedData}
                    ]}
                });
            return res.data
        });
    }, []);

    // useEffect(() => {
    //     if(energyComparison){
    //         console.log(energyComparison)
    //         new Chart(canvasRef.current, 
    //             {
    //                 type: 'line', 
    //                 data: {labels: months, datasets: [
    //                     {label: "baseline", data: energyComparison.baseline.map(usage => usage.energy)},
    //                     {label: "improved", data: energyComparison.improved.map(usage => usage.energy)}
    //                 ]}
    //             });
    //     }
    // }, [energyComparison]);

    return (
      <div>
        <canvas ref={canvasRef} id="energy_comparison"></canvas>
      </div>
    );
  }
  
export default EnergyComparisonChart;
  