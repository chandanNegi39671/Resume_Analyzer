import { useState, useCallback } from 'react';
import { analyzeResume } from '../utils/api';

/**
 * Custom hook for resume analysis state and logic.
 */
export const useAnalyzer = () => {
  const [file, setFile] = useState(null);
  const [jdText, setJdText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  /**
   * Validates the input file and JD text.
   * @returns {Object} { valid: boolean, errors: Object }
   */
  const validate = useCallback(() => {
    const errors = {};
    
    // File validation
    if (!file) {
      errors.file = 'Please upload a resume file.';
    } else {
      const allowedTypes = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      ];
      if (!allowedTypes.includes(file.type)) {
        errors.file = 'Only PDF and DOCX files are accepted.';
      }
      if (file.size > 5 * 1024 * 1024) {
        errors.file = 'File size must be less than 5MB.';
      }
    }

    // JD validation
    if (!jdText || jdText.trim().length < 50) {
      errors.jdText = 'Job description must be at least 50 characters.';
    } else if (jdText.length > 5000) {
      errors.jdText = 'Job description must be less than 5000 characters.';
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors,
    };
  }, [file, jdText]);

  /**
   * Calls the analysis API and updates state.
   */
  const analyze = async () => {
    const { valid } = validate();
    if (!valid) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeResume(file, jdText);
      setResult(data);
      return data;
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during analysis.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Resets the analyzer state.
   */
  const reset = useCallback(() => {
    setFile(null);
    setJdText('');
    setIsLoading(false);
    setError(null);
    setResult(null);
  }, []);

  return {
    file,
    setFile,
    jdText,
    setJdText,
    isLoading,
    error,
    result,
    validate,
    analyze,
    reset,
  };
};
