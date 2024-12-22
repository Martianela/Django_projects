import { formatDistanceToNow } from "date-fns";
import PropTypes from "prop-types";

function JobCard({ jobdata }) {
  // Calculate the time difference from the posted date
  const postedDate =
    jobdata?.posted_date && !isNaN(new Date(jobdata.posted_date))
      ? formatDistanceToNow(new Date(jobdata.posted_date), { addSuffix: true })
      : jobdata?.posted_date;

  return (
    <div className="bg-white p-2 rounded-xl hover:border border-blue-500">
      <div className="flex gap-2 items-center px-3">
        <span className="font-light">{postedDate}</span>
        <span className="bg-[#f4edff] px-4 py-1 text-violet-600 text-xs rounded-3xl">
          {jobdata.location}
        </span>
      </div>
      <div className="bg-gray-50 rounded-b-xl px-8 mt-2 py-6 flex justify-between items-center">
        <div className="flex gap-3 items-center">
          <img
            className="w-14 h-14 rounded-full object-cover"
            src="https://images.pexels.com/photos/21326994/pexels-photo-21326994/free-photo-of-display-of-leather-bags.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
            alt="Company Logo"
          />
          <div>
            <h4 className="text-xl">{jobdata.title || "No Title Available"}</h4>
            <p>{jobdata.company_name || "Unknown Company"}</p>
          </div>
        </div>
        <div className="flex flex-col gap-1 text-right">
          <h5 className="text-lg flex-1">{jobdata.pay_details || "N/A"}</h5>
          <p className="font-light flex-1">
            {jobdata.employment_details || "Employment details not available"}
          </p>
        </div>
      </div>
    </div>
  );
}

// Add prop validation
JobCard.propTypes = {
  jobdata: PropTypes.shape({
    posted_date: PropTypes.string.isRequired, // Ensure `posted_date` is a string
    location: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    company_name: PropTypes.string,
    pay_details: PropTypes.string,
    employment_details: PropTypes.string,
  }).isRequired,
};

export default JobCard;
