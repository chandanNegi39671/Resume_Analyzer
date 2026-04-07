import React, { useState } from 'react';
import UploadForm from './components/upload/UploadForm';
import ScoreOverview from './components/dashboard/ScoreOverview';
import ATSPanel from './components/dashboard/ATSPanel';
import MatchPanel from './components/dashboard/MatchPanel';
import ProjectsPanel from './components/dashboard/ProjectsPanel';
import ShortlistPanel from './components/dashboard/ShortlistPanel';
import ImprovementPanel from './components/dashboard/ImprovementPanel';
import VerdictPanel from './components/dashboard/VerdictPanel';
import { AlertTriangle, RefreshCw } from 'lucide-react';

const App = () => {
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleReset = () => {
    setAnalysisResult(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans antialiased">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-2">
              <div className="bg-indigo-600 p-1.5 rounded-lg">
                <RefreshCw className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold tracking-tight text-gray-900">ResumeAnalyzer</span>
            </div>
            {analysisResult && (
              <button
                onClick={handleReset}
                className="text-sm font-medium text-indigo-600 hover:text-indigo-500 flex items-center space-x-1"
              >
                <span>New Analysis</span>
              </button>
            )}
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!analysisResult ? (
          <div className="py-12">
            <UploadForm onResult={setAnalysisResult} />
          </div>
        ) : (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Incomplete Analysis Warning Banner */}
            {analysisResult.meta?.incomplete === true && (
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-lg shadow-sm flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-yellow-500 mt-0.5" />
                <div>
                  <h3 className="text-sm font-bold text-yellow-800">Analysis may be incomplete</h3>
                  <p className="text-sm text-yellow-700">Some sections could not be fully processed due to technical limits or input complexity.</p>
                </div>
              </div>
            )}

            {/* Dashboard Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Main Column */}
              <div className="lg:col-span-8 space-y-8">
                <ScoreOverview result={analysisResult} />
                <ImprovementPanel result={analysisResult} />
                <VerdictPanel result={analysisResult} />
              </div>

              {/* Sidebar Column */}
              <div className="lg:col-span-4 space-y-8">
                <ShortlistPanel result={analysisResult} />
                <ATSPanel result={analysisResult} />
                <MatchPanel result={analysisResult} />
                <ProjectsPanel result={analysisResult} />
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-gray-200 py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
          <p>© 2026 Resume Analyzer Project. Built with React, Tailwind CSS, and FastAPI.</p>
        </div>
      </footer>
    </div>
  );
};

export default App;
