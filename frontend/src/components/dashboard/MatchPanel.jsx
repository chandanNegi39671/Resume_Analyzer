import React from 'react';
import { getScoreColor, getScoreBgColor } from '../../utils/scoreColors';
import { Target, Check, X, Shield, BookOpen, UserCheck } from 'lucide-react';

const Tag = ({ label, color }) => (
  <span className={`px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-tight ${color}`}>
    {label}
  </span>
);

const AlignmentScore = ({ label, score, explanation, icon }) => {
  const IconComponent = icon
  return (
  <div className="bg-gray-50 rounded-xl p-4 border border-gray-100 space-y-2">
    <div className="flex justify-between items-center">
      <div className="flex items-center space-x-2">
        <IconComponent className="w-4 h-4 text-indigo-500" />
        <span className="text-xs font-bold text-gray-800 uppercase tracking-tight">{label}</span>
      </div>
      <span className={`text-sm font-black ${getScoreColor(score)}`}>{score}%</span>
    </div>
    <div className="h-1.5 bg-white rounded-full overflow-hidden border border-gray-100">
      <div 
        className={`h-full transition-all duration-700 ease-out ${getScoreBgColor(score)}`}
        style={{ width: `${score}%` }}
      />
    </div>
    <p className="text-xs text-gray-600 leading-relaxed italic">{explanation}</p>
  </div>
  )
};

const MatchPanel = ({ result }) => {
  const { match_analysis } = result;
  const { 
    overall_match_score, 
    skills_match, 
    experience_alignment, 
    education_alignment, 
    domain_alignment, 
    keyword_coverage 
  } = match_analysis;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-6 border-b border-gray-50">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-bold text-gray-900">Job Match Analysis</h3>
          <div className="flex flex-col items-end">
            <span className={`text-2xl font-black ${getScoreColor(overall_match_score)}`}>{overall_match_score}</span>
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Match Score</span>
          </div>
        </div>

        <div className="space-y-4">
          {/* Skills Tags Section */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-gray-800 uppercase tracking-widest flex items-center">
              <Target className="w-3.5 h-3.5 mr-1.5 text-indigo-500" />
              Skills Alignment
            </h4>
            
            <div className="space-y-4">
              {/* Matched Skills */}
              {skills_match?.matched_skills?.length > 0 && (
                <div>
                  <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-tight mb-2">Matched Skills</label>
                  <div className="flex flex-wrap gap-1.5">
                    {skills_match.matched_skills.map((skill, idx) => (
                      <Tag key={idx} label={skill} color="bg-emerald-100 text-emerald-700 border border-emerald-200" />
                    ))}
                  </div>
                </div>
              )}

              {/* Missing Required Skills */}
              {skills_match?.missing_required_skills?.length > 0 && (
                <div>
                  <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-tight mb-2">Missing (Required)</label>
                  <div className="flex flex-wrap gap-1.5">
                    {skills_match.missing_required_skills.map((skill, idx) => (
                      <Tag key={idx} label={skill} color="bg-red-100 text-red-700 border border-red-200" />
                    ))}
                  </div>
                </div>
              )}

              {/* Missing Preferred Skills */}
              {skills_match?.missing_preferred_skills?.length > 0 && (
                <div>
                  <label className="block text-[10px] font-bold text-gray-400 uppercase tracking-tight mb-2">Missing (Preferred)</label>
                  <div className="flex flex-wrap gap-1.5">
                    {skills_match.missing_preferred_skills.map((skill, idx) => (
                      <Tag key={idx} label={skill} color="bg-blue-100 text-blue-700 border border-blue-200" />
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Keyword Coverage */}
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <h4 className="text-xs font-bold text-gray-800 uppercase tracking-widest">Keyword Coverage</h4>
            <span className={`text-sm font-black ${getScoreColor(keyword_coverage?.score || 0)}`}>{keyword_coverage?.score || 0}%</span>
          </div>
          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
            <div 
              className={`h-full transition-all duration-700 ease-out ${getScoreBgColor(keyword_coverage?.score || 0)}`}
              style={{ width: `${keyword_coverage?.score || 0}%` }}
            />
          </div>
          <div className="grid grid-cols-2 gap-4 pt-2">
            <div>
              <span className="block text-[10px] font-bold text-gray-400 uppercase mb-2">Present</span>
              <ul className="space-y-1">
                {keyword_coverage?.important_keywords_present?.slice(0, 5).map((kw, idx) => (
                  <li key={idx} className="text-[11px] text-emerald-700 flex items-center">
                    <Check className="w-2.5 h-2.5 mr-1 text-emerald-500" /> {kw}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <span className="block text-[10px] font-bold text-gray-400 uppercase mb-2">Missing</span>
              <ul className="space-y-1">
                {keyword_coverage?.important_keywords_missing?.slice(0, 5).map((kw, idx) => (
                  <li key={idx} className="text-[11px] text-red-700 flex items-center">
                    <X className="w-2.5 h-2.5 mr-1 text-red-500" /> {kw}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Alignment Sections */}
        <div className="space-y-4 pt-2">
          <AlignmentScore 
            label="Experience Alignment" 
            score={experience_alignment?.score || 0}
            explanation={experience_alignment?.explanation}
            icon={Shield}
          />
          <AlignmentScore 
            label="Domain Alignment" 
            score={domain_alignment?.score || 0}
            explanation={domain_alignment?.explanation}
            icon={UserCheck}
          />
          <AlignmentScore 
            label="Education Alignment" 
            score={education_alignment?.score || 0}
            explanation={education_alignment?.explanation}
            icon={BookOpen}
          />
        </div>
      </div>
    </div>
  );
};

export default MatchPanel;
