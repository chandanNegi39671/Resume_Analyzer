import React from 'react';
import { getScoreRingColor } from '../../utils/scoreColors';

const CircularProgress = ({ score, label, size = 120 }) => {
  const radius = (size - 10) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const strokeColor = getScoreRingColor(score);

  return (
    <div className="flex flex-col items-center space-y-3">
      <div className="relative" style={{ width: size, height: size }}>
        {/* Background Ring */}
        <svg className="w-full h-full transform -rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="transparent"
            stroke="currentColor"
            strokeWidth="8"
            className="text-gray-100"
          />
          {/* Progress Ring */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="transparent"
            stroke={strokeColor}
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        {/* Score Number */}
        <div className="absolute inset-0 flex items-center justify-center flex-col">
          <span className="text-2xl font-bold text-gray-900">{score}</span>
          <span className="text-[10px] uppercase tracking-wider text-gray-500 font-semibold">/ 100</span>
        </div>
      </div>
      <span className="text-sm font-semibold text-gray-600 text-center">{label}</span>
    </div>
  );
};

const ScoreOverview = ({ result }) => {
  const { ats_analysis, match_analysis, project_analysis, shortlist_estimation, final_verdict } = result;

  return (
    <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900">Score Overview</h2>
          <p className="text-sm text-gray-500">Comprehensive analysis of your resume performance.</p>
        </div>
        <div className="flex items-center space-x-3 bg-indigo-50 px-4 py-2 rounded-full border border-indigo-100">
          <span className="text-sm font-medium text-indigo-700">Overall Grade:</span>
          <span className={`text-sm font-bold uppercase tracking-wider px-2 py-0.5 rounded ${
            final_verdict?.overall_grade === 'Excellent' ? 'bg-emerald-500 text-white' :
            final_verdict?.overall_grade === 'Strong' ? 'bg-green-500 text-white' :
            final_verdict?.overall_grade === 'Good' ? 'bg-yellow-500 text-white' :
            final_verdict?.overall_grade === 'Fair' ? 'bg-amber-500 text-white' :
            'bg-red-500 text-white'
          }`}>
            {final_verdict?.overall_grade || 'N/A'}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        <CircularProgress
          score={ats_analysis?.ats_score || 0}
          label="ATS Score"
        />
        <CircularProgress
          score={match_analysis?.overall_match_score || 0}
          label="Job Match Score"
        />
        <CircularProgress
          score={project_analysis?.overall_project_relevance_score || 0}
          label="Project Relevance"
        />
        
        {/* Shortlist Probability - Special Display */}
        <div className="flex flex-col items-center space-y-3">
          <div className="w-[120px] h-[120px] rounded-full border-8 border-indigo-50 flex flex-col items-center justify-center bg-indigo-50/30">
            <span className="text-xl font-black text-indigo-600">{shortlist_estimation?.probability_label || '0%'}</span>
            <div className={`mt-1 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-widest ${
              shortlist_estimation?.confidence === 'high' ? 'bg-emerald-100 text-emerald-700' :
              shortlist_estimation?.confidence === 'medium' ? 'bg-yellow-100 text-yellow-700' :
              'bg-amber-100 text-amber-700'
            }`}>
              {shortlist_estimation?.confidence || 'Low'}
            </div>
          </div>
          <span className="text-sm font-semibold text-gray-600 text-center">Shortlist Probability</span>
        </div>
      </div>
    </div>
  );
};

export default ScoreOverview;
