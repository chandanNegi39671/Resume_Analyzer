import React from 'react';
import { getScoreColor, getScoreBgColor, getSeverityBadgeColor } from '../../utils/scoreColors';
import { AlertCircle, CheckCircle, Info } from 'lucide-react';

const SubScoreBar = ({ label, score }) => (
  <div className="space-y-1.5">
    <div className="flex justify-between items-center text-xs font-medium text-gray-500">
      <span>{label}</span>
      <span className="font-bold text-gray-700">{score}%</span>
    </div>
    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
      <div 
        className={`h-full transition-all duration-700 ease-out ${getScoreBgColor(score)}`}
        style={{ width: `${score}%` }}
      />
    </div>
  </div>
);

const ATSPanel = ({ result }) => {
  const { ats_analysis } = result;
  const { ats_score, ats_grade, is_ats_friendly, issues, formatting_score, keyword_density_score, section_structure_score } = ats_analysis;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-6 border-b border-gray-50">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-bold text-gray-900">ATS Analysis</h3>
          <div className="flex flex-col items-end">
            <span className={`text-2xl font-black ${getScoreColor(ats_score)}`}>{ats_score}</span>
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{ats_grade}</span>
          </div>
        </div>

        <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium ${
          is_ats_friendly ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'
        }`}>
          {is_ats_friendly ? (
            <CheckCircle className="w-4 h-4" />
          ) : (
            <AlertCircle className="w-4 h-4" />
          )}
          <span>{is_ats_friendly ? 'ATS-Friendly Structure' : 'ATS-Incompatible Elements Found'}</span>
        </div>
      </div>

      <div className="p-6 space-y-6">
        <div className="space-y-4">
          <SubScoreBar label="Formatting & Layout" score={formatting_score} />
          <SubScoreBar label="Keyword Density" score={keyword_density_score} />
          <SubScoreBar label="Section Structure" score={section_structure_score} />
        </div>

        <div className="pt-2">
          <h4 className="text-sm font-bold text-gray-800 mb-3 flex items-center">
            Detected Issues
            <span className="ml-2 px-1.5 py-0.5 bg-gray-100 text-gray-500 rounded text-[10px] font-bold">
              {issues?.length || 0}
            </span>
          </h4>
          
          {issues && issues.length > 0 ? (
            <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
              {issues.map((issue, idx) => (
                <div key={idx} className="p-4 bg-gray-50 rounded-xl border border-gray-100 space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="text-xs font-bold text-gray-800 uppercase tracking-tight">
                      {issue.issue_type}
                    </span>
                    <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full border ${getSeverityBadgeColor(issue.severity)}`}>
                      {issue.severity}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 leading-relaxed">{issue.description}</p>
                  <div className="flex items-start space-x-2 bg-white/60 p-2 rounded-lg border border-gray-100">
                    <Info className="w-4 h-4 text-indigo-400 mt-0.5 flex-shrink-0" />
                    <p className="text-xs text-indigo-600 font-medium italic">
                      <span className="font-bold not-italic mr-1">Rec:</span>
                      {issue.recommendation}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-6 bg-emerald-50 rounded-xl border border-emerald-100">
              <CheckCircle className="w-8 h-8 text-emerald-500 mx-auto mb-2 opacity-50" />
              <p className="text-sm font-medium text-emerald-700">No ATS issues detected</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ATSPanel;
