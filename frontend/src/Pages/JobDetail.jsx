import { useEffect, useState } from "react";
import Navbar from "../Components/Navbar";
import axios from "axios";
import { useParams } from "react-router-dom";

function JobDetail() {
  const [details, setDetails] = useState(null);
  const { id } = useParams();
  useEffect(() => {
    async function fetchDetail() {
      const res = await axios.get(`http://127.0.0.1:8000/api/jobs/${id}/`);
      console.log(res);
      const skillsArray = res.data.skills.split(", ");
      console.log(skillsArray);
      setDetails({ ...res.data, skills: skillsArray });
    }
    fetchDetail();
  }, [id]);
  console.log(details);

  return (
    <>
      <Navbar />
      {details === null ? (
        <p>Job Details Not Found</p>
      ) : (
        <div className="max-w-6xl mx-auto mt-10 bg-white rounded-2xl p-2">
          <div className="">
            <div className="rounded-2xl bg-gray-50 flex items-center justify-between px-5">
              <img
                className="w-16 h-16 rounded-full relative top-10"
                src="https://images.pexels.com/photos/4744755/pexels-photo-4744755.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
                alt="log"
              />
              <div className="relative top-10 flex gap-2">
                <button className="bg-blue-600 px-8 text-sm py-2  rounded-full text-white">
                  Apply
                </button>
                <button className="capitalize border-gray-600/20 text-gray-700 border px-8 text-sm py-2  rounded-full">
                  Share job
                </button>
              </div>
            </div>
            <div className="mt-12 p-5">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-2xl">{details?.title}</h3>
                  <a href={details?.company_profile_url}>
                    {details?.company_name}
                  </a>
                </div>
                <div className="text-right">
                  <h5 className="text-lg">{details?.pay_details}</h5>
                  <div className="flex gap-3 font-light text-sm">
                    <p>
                      <span>{details?.location}</span>
                    </p>
                    <p>{details?.posted_date}</p>
                    <p>{details?.employment_details}</p>
                  </div>
                </div>
              </div>

              <div className="mt-10 flex flex-col gap-10">
                <div>
                  <h3 className="text-lg capitalize">skills Required</h3>
                  <div className=" mt-3 flex gap-3">
                    {details?.skills.map((e, index) => {
                      return (
                        <span
                          key={e + index}
                          className="px-4 py-1 bg-gray-50 rounded-full text-gray-600 text-sm"
                        >
                          {e}bj
                        </span>
                      );
                    })}
                  </div>
                </div>
                <div>
                  <h3 className="text-lg capitalize">skills Required</h3>
                  <p className="text-sm text-gray-700 mt-2">
                    {details.job_description}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
export default JobDetail;
