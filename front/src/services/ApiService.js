import axios from "axios";

export default function getEnergyComparison(){
    axios
    .get("http://127.0.0.1:8000/api/before_after_energy_usage/1e0e7511-9e40-4b13-8c52-4f9c26c41c55")
    .then(res => {
        console.log(res.data)
        return res.data
    });
}