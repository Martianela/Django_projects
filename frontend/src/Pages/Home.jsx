import { useEffect, useState } from "react";
import Navbar from "../Components/Navbar";
import axios from "axios";
import JobCard from "./JobCard";
import { Link } from "react-router-dom";

function Home() {
  const [jobs, setJobs] = useState([]); // All jobs from API
  const [searchQuery, setSearchQuery] = useState(""); // Search query input
  const [filteredJobs, setFilteredJobs] = useState([]); // Jobs filtered by search

  // Fetch jobs from API
  useEffect(() => {
    async function getData() {
      const res = await axios.get("http://127.0.0.1:8000/api/jobs/");
      console.log(res.data);
      setJobs(res.data);
      setFilteredJobs(res.data); // Initialize filtered jobs with all jobs
    }
    getData();
  }, []);

  // Update filtered jobs based on search query
  useEffect(() => {
    setFilteredJobs(
      jobs.filter((job) =>
        job.title.toLowerCase().includes(searchQuery.toLowerCase())
      )
    );
  }, [searchQuery, jobs]);

  return (
    <div className="bg-gray-100">
      <Navbar />
      <div className="max-w-6xl mx-auto">
        <div className="bg-white border rounded-xl p-2 mt-10">
          <div className="p-6 bg-gray-100 rounded-lg">
            <div className="flex border hover:border-blue-600 rounded-full overflow-hidden">
              <input
                className="px-6 py-3 w-full outline-none font-light"
                placeholder="Search by title"
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)} // Update search query
              />
              <button className="bg-blue-600 text-white px-10">Search</button>
            </div>
          </div>
        </div>
        <div className="mt-5 flex flex-col gap-5 py-10">
          {filteredJobs.map((job) => (
            <Link key={job.id} to={`/job/${job.id}/`}>
              <JobCard jobdata={job} />
            </Link>
          ))}
          {filteredJobs.length === 0 && (
            <p className="text-gray-500 text-center">No jobs found.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;
