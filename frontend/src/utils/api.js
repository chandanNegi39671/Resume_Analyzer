const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Analyzes a resume against a job description.
 * @param {File} file - The resume file (PDF or DOCX).
 * @param {string} jdText - The job description text.
 * @returns {Promise<Object>} - The structured JSON analysis result.
 */
export const analyzeResume = async (file, jdText) => {
  const formData = new FormData();
  formData.append('resume_file', file);
  formData.append('jd_text', jdText);

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 35000); // 35 second timeout

  try {
    const response = await fetch(`${BASE_URL}/api/analyze`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { message: 'An unexpected error occurred.' };
      }
      
      throw {
        error: errorData.error || 'server_error',
        message: errorData.message || 'The server returned an error.',
        code: errorData.code || `ERR_${response.status}`,
      };
    }

    return await response.json();
  } catch (err) {
    clearTimeout(timeoutId);
    
    if (err.name === 'AbortError') {
      throw {
        error: 'timeout',
        message: 'The request took too long. Please try again.',
        code: 'TIMEOUT_001',
      };
    }

    if (err.error) throw err;

    throw {
      error: 'network_error',
      message: 'Could not reach the server. Please try again.',
      code: 'NET_001',
    };
  }
};
