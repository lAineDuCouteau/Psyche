import React, { useEffect, useState } from "react";
import axios from "axios";
import styles from "./surveyDetails.module.scss";
import { useParams, useNavigate } from "react-router-dom";

interface Survey {
  _id: string;
  title: string;
  description: string;
  sections: {
    questions: {
      _id: string;
      questionText: string;
      choices: string[];
    }[];
  }[];
}

interface SelectedAnswers {
  [questionId: string]: string; // Selected choice
}

const SurveyDetails: React.FC = () => {
  const { surveyId } = useParams<{ surveyId: string }>();
  const navigate = useNavigate();
  const [survey, setSurvey] = useState<Survey | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<SelectedAnswers>({});
  const [loading, setLoading] = useState<boolean>(true);

  // Fetch survey details
  useEffect(() => {
    const fetchSurveyDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/surveys/${surveyId}`);
        console.log("Survey Details:", response.data); // Debugging API response
        setSurvey(response.data);
      } catch (error) {
        console.error("Error fetching survey details:", error);
        alert("Failed to load survey details. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (surveyId) fetchSurveyDetails();
  }, [surveyId]);

  // Handle answer selection
  const handleAnswerChange = (questionId: string, choice: string) => {
    setSelectedAnswers((prevState) => ({
      ...prevState,
      [questionId]: choice,
    }));
  };

  // Submit the survey
  const handleSubmit = async () => {
    if (!survey) return;

    const userId = localStorage.getItem("userId");

    if (!userId) {
      alert("User is not logged in.");
      return;
    }

    const responses = Object.entries(selectedAnswers).map(([questionId, choice]) => ({
      questionId,
      choice,
    }));

    try {
      await axios.post("http://localhost:5000/api/response/surveys/submit", {
        surveyId: survey._id,
        responses,
        userId,
      });

      // After successfully submitting the survey, add the survey ID to the answered surveys list
      const answeredSurveys = JSON.parse(localStorage.getItem("answeredSurveys") || "[]");
      answeredSurveys.push(survey._id);
      localStorage.setItem("answeredSurveys", JSON.stringify(answeredSurveys));

      alert("Survey submitted successfully!");

      navigate("/surveyDashboard");

    } catch (error) {
      alert(`Failed to submit survey. Error: ${error}`);
    }
  };

  if (loading) {
    return <p>Loading survey details...</p>;
  }

  if (!survey) {
    return <p>Survey not found or failed to load.</p>;
  }

  return (
    <div className={styles.surveyDetailsContainer}>
      <h2>{survey.title}</h2>
      <p>{survey.description}</p>
      {survey.sections.map((section, sectionIndex) => (
        <div key={sectionIndex} className={styles.section}>
          {section.questions.map((question) => (
            <div key={question._id} className={styles.question}>
              <p>{question.questionText}</p>
              {question.choices.map((choice, index) => (
                <label key={index} className={styles.choice}>
                  <input
                    type="radio"
                    name={`question-${question._id}`}
                    value={choice}
                    checked={selectedAnswers[question._id] === choice}
                    onChange={() => handleAnswerChange(question._id, choice)}
                  />
                  {choice}
                </label>
              ))}
            </div>
          ))}
        </div>
      ))}
      <button className={styles.submitButton} onClick={handleSubmit}>
        Submit Survey
      </button>
    </div>
  );
};

export default SurveyDetails;
