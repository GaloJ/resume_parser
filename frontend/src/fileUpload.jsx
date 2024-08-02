// fileUpload.jsx
import React, { useState} from 'react';

function fileUpload() {
  const [file, setFile] = useState(null);
  const [job_post, setJobPost] = useState('');
  const [message, setMessage] = useState('');
  const [pdfUrl, setPdfUrl] = useState('');
  const [matchPercent, setPercent] = useState('');
  const [matchWords, setMatch] = useState([]);
  const [noMatchWords, setNoMatch] = useState([]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleTextChange = (event) => {
    setJobPost(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_post', job_post);
    
    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      });
      const result = await response.json();
      console.log("Response Result:", result.message);  // Debugging line
      setMessage(result.message || result.error);
  
      if (result.file_url) {
          setPdfUrl(result.file_url);
        }

      if (result.match_percentage) {
        setPercent(result.match_percentage);
      }

      if (result.match_words) {
        setMatch(result.match_words);
      }

      if (result.non_match_words) {
        setNoMatch(result.non_match_words);
      }

    } catch (error) {
      setMessage('An error occurred');
    }
  };

  return (
    <div>
      <h1>ATS Resume Checker</h1>
      <h2>Upload your resume and paste a job post</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept="application/pdf" />
        <button type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
      <table>
        <tr>
        <td rowSpan={3}>
              <textarea
              className="fixed-textarea"
              placeholder="Job description here"
              onChange={handleTextChange}
              value={job_post}
            />
        </td>   
        <td rowSpan={3}>
          {pdfUrl && (
            <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center',width: '1000px',height: '800px'}}>
              <iframe
                src={pdfUrl}
                style={{ width: '100%', height: '100%', border: 'none' }}
                title="Uploaded PDF"
              />
            </div>
          )}
        </td>
        <td>
          {matchPercent && <p>Match Score</p>}
          {matchPercent && <p>{matchPercent}</p>}
        </td>
        </tr>
        <tr>
          <td> 
          {matchWords.length > 0 && <p>Matched Words</p>}
          {matchWords && 
            <ul className="no-bullets">
            {matchWords.map((matchWords, index) => (
              <li key={index}>{matchWords}</li>
            ))}
            </ul>}
          </td>
        </tr>
        <tr>
          <td>
            {noMatchWords.length > 0 && <p>Missing Words</p>}
            {noMatchWords && 
            <ul className="no-bullets">
            {noMatchWords.map((noMatchWords, index) => (
            <li key={index}>{noMatchWords}</li>
            ))}
            </ul>}
          </td>
        </tr>
      </table>
    </div>
  );
}

export default fileUpload;