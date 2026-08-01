import axios from "axios";

// This is a placeholder Axios instance.
// When the backend is ready, just update the baseURL below
// and start replacing mock data calls in services/ with real requests.
const apiClient = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
