import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  getPatient,
  createPatient,
  updatePatient,
} from "@/api/patients";

interface PatientFormProps {
  editMode?: boolean;
}

const PatientForm: React.FC<PatientFormProps> = ({ editMode = false }) => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [formValues, setFormValues] = useState({
    medical_record_number: "",
    first_name: "",
    last_name: "",
    date_of_birth: "",
  });
  const [loading, setLoading] = useState(editMode);

  useEffect(() => {
    if (editMode && id) {
      getPatient(Number(id))
        .then((p) => {
          setFormValues({
            medical_record_number: p.medical_record_number,
            first_name: p.first_name,
            last_name: p.last_name,
            date_of_birth: p.date_of_birth,
          });
        })
        .catch((err) => console.error("Fetch patient failed:", err))
        .finally(() => setLoading(false));
    }
  }, [editMode, id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormValues({
      ...formValues,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editMode && id) {
        await updatePatient(Number(id), formValues);
      } else {
        await createPatient(formValues);
      }
      navigate("/patients");
    } catch (err) {
      console.error("Submit failed:", err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full text-gray-500">
        Loading form...
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-4">
        {editMode ? "Edit Patient" : "New Patient"}
      </h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">MRN</label>
          <input
            type="text"
            name="medical_record_number"
            value={formValues.medical_record_number}
            onChange={handleChange}
            required
            className="mt-1 w-full border px-3 py-2 rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium">First Name</label>
          <input
            type="text"
            name="first_name"
            value={formValues.first_name}
            onChange={handleChange}
            required
            className="mt-1 w-full border px-3 py-2 rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Last Name</label>
          <input
            type="text"
            name="last_name"
            value={formValues.last_name}
            onChange={handleChange}
            required
            className="mt-1 w-full border px-3 py-2 rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Date of Birth</label>
          <input
            type="date"
            name="date_of_birth"
            value={formValues.date_of_birth}
            onChange={handleChange}
            required
            className="mt-1 w-full border px-3 py-2 rounded"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          {editMode ? "Update Patient" : "Create Patient"}
        </button>
      </form>
    </div>
  );
};

export default PatientForm;
