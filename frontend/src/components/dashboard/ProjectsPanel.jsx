import React, { useState } from 'react';
import { getRelevanceBadgeColor, getScoreColor } from '../../utils/scoreColors';
import { Briefcase, ChevronDown, ChevronUp, Sparkles, MessageSquare } from 'lucide-react';

const ProjectCard = ({ project }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const badgeClass = getRelevanceBadgeColor(project.relevance_to_jd);

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300">
      <div className="p-5">
        <div className="flex justify-between items-start mb-3">
          <div className="flex-1">
            <h4 className="text-sm font-bold text-gray-900 line-clamp-1">{project.project_name}</h4>
            <div className="flex items-center mt-1.5 space-x-2">
              <span className={`text-[10px] px-2 py-0.5 rounded-full border font-bold uppercase tracking-wider ${badgeClass}`}>
                {project.relevance_to_jd}
              </span>
              <span className={`text-[10px] font-bold ${getScoreColor(project.relevance_score)}`}>
                {project.relevance_score}% Relevant
              </span>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-start space-x-2">
            <MessageSquare className="w-3.5 h-3.5 text-gray-400 mt-0.5 flex-shrink-0" />
            <p className="text-xs text-gray-600 leading-relaxed italic">{project.why_relevant}</p>
          </div>

          {project.rewrite_suggestion && (
            <div className="pt-2 border-t border-gray-50">
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="flex items-center justify-between w-full text-[10px] font-bold text-indigo-600 uppercase tracking-widest hover:text-indigo-700 transition-colors"
              >
                <span className="flex items-center">
                  <Sparkles className="w-3 h-3 mr-1.5" />
                  Rewrite Suggestion
                </span>
                {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
              </button>
              
              {isExpanded && (
                <div className="mt-3 p-3 bg-indigo-50/50 rounded-lg border border-indigo-100/50 animate-in fade-in slide-in-from-top-2 duration-300">
                  <p className="text-xs text-gray-700 leading-relaxed font-medium">
                    {project.rewrite_suggestion}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const ProjectsPanel = ({ result }) => {
  const { project_analysis } = result;
  const { projects_found, projects, overall_project_relevance_score } = project_analysis;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-6 border-b border-gray-50">
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center space-x-2">
            <Briefcase className="w-5 h-5 text-indigo-500" />
            <h3 className="text-lg font-bold text-gray-900">Project Relevance</h3>
          </div>
          <div className="flex flex-col items-end">
            <span className={`text-2xl font-black ${getScoreColor(overall_project_relevance_score)}`}>{overall_project_relevance_score}</span>
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Avg Relevance</span>
          </div>
        </div>
        <p className="text-xs text-gray-500 font-medium">
          Found {projects_found} {projects_found === 1 ? 'project' : 'projects'} in your resume.
        </p>
      </div>

      <div className="p-6">
        {projects && projects.length > 0 ? (
          <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
            {projects.map((project, idx) => (
              <ProjectCard key={idx} project={project} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
            <Briefcase className="w-12 h-12 text-gray-300 mx-auto mb-3 opacity-50" />
            <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">No projects detected</p>
            <p className="text-xs text-gray-500 mt-1 max-w-[200px] mx-auto">
              Consider adding specific projects to boost your match score.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectsPanel;
