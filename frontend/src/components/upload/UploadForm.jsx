import React, { useState, useEffect } from 'react';
import { useAnalyzer } from '../../hooks/useAnalyzer';
import { Upload, FileText, X, AlertCircle, Loader2 } from 'lucide-react';

const UploadForm = ({ onResult }) => {
  const {
    file,
    setFile,
    jdText,
    setJdText,
    isLoading,
    error,
    validate,
    analyze,
  } = useAnalyzer();

  const [validationErrors, setValidationErrors] = useState({});
  const [isDragging, setIsDragging] = useState(false);

  // Re-validate on change to update UI errors
  useEffect(() => {
    if (file || jdText) {
      const { errors } = validate();
      setValidationErrors(errors);
    }
  }, [file, jdText, validate]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { valid, errors } = validate();
    setValidationErrors(errors);

    if (valid) {
      try {
        const data = await analyze();
        if (data) {
          onResult(data);
        }
      } catch {
        // Error handled by hook state
      }
    }
  };

  const isFormValid = file && jdText.trim().length >= 50 && jdText.length <= 5000 && Object.keys(validationErrors).length === 0;

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-xl shadow-lg border border-gray-100">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Resume Analyzer</h1>
        <p className="text-gray-600">Upload your resume and job description to get AI-powered insights.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Resume Upload Section */}
        <div className="space-y-2">
          <label className="block text-sm font-semibold text-gray-700 mb-1">
            Resume (PDF or DOCX)
          </label>
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className={`relative border-2 border-dashed rounded-lg p-8 transition-all duration-200 text-center ${
              isDragging ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-indigo-400'
            } ${file ? 'bg-gray-50' : ''} ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileChange}
              disabled={isLoading}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
            />
            {!file ? (
              <div className="space-y-3">
                <div className="mx-auto w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
                  <Upload className="w-6 h-6 text-indigo-600" />
                </div>
                <div className="text-sm text-gray-600">
                  <span className="font-semibold text-indigo-600">Click to browse</span> or drag and drop
                  <p className="text-xs text-gray-400 mt-1">PDF or DOCX (Max 5MB)</p>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center space-x-3">
                <FileText className="w-8 h-8 text-indigo-500" />
                <div className="text-left">
                  <p className="text-sm font-medium text-gray-900 truncate max-w-[200px]">{file.name}</p>
                  <p className="text-xs text-gray-500">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                </div>
                <button
                  type="button"
                  onClick={(e) => { e.preventDefault(); setFile(null); }}
                  disabled={isLoading}
                  className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                >
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              </div>
            )}
          </div>
          {validationErrors.file && (
            <p className="text-xs text-red-500 flex items-center mt-1">
              <AlertCircle className="w-3 h-3 mr-1" /> {validationErrors.file}
            </p>
          )}
        </div>

        {/* Job Description Section */}
        <div className="space-y-2">
          <div className="flex justify-between items-end mb-1">
            <label className="block text-sm font-semibold text-gray-700">
              Job Description
            </label>
            <span className={`text-xs ${jdText.length > 5000 || jdText.length < 50 ? 'text-amber-600' : 'text-gray-400'}`}>
              {jdText.length} / 5000 characters
            </span>
          </div>
          <textarea
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            disabled={isLoading}
            placeholder="Paste the job description here (min 50 chars)..."
            className={`w-full h-48 px-4 py-3 rounded-lg border focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all duration-200 resize-none ${
              validationErrors.jdText ? 'border-red-300 bg-red-50' : 'border-gray-300'
            } disabled:bg-gray-50 disabled:cursor-not-allowed`}
          />
          {validationErrors.jdText && (
            <p className="text-xs text-red-500 flex items-center mt-1">
              <AlertCircle className="w-3 h-3 mr-1" /> {validationErrors.jdText}
            </p>
          )}
        </div>

        {/* Submit Section */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={!isFormValid || isLoading}
            className={`w-full py-4 rounded-lg font-bold text-white shadow-md transition-all duration-200 flex items-center justify-center space-x-2 ${
              !isFormValid || isLoading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-700 active:transform active:scale-[0.98]'
            }`}
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <span>Analyze Resume</span>
            )}
          </button>
          
          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-2">
              <AlertCircle className="w-5 h-5 text-red-500 mt-0.5" />
              <div className="text-sm text-red-700">
                <p className="font-semibold">Analysis failed</p>
                <p>{error}</p>
              </div>
            </div>
          )}
        </div>
      </form>
    </div>
  );
};

export default UploadForm;
