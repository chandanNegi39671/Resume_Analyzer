import React from 'react';
import { Shield, CheckCircle2, XCircle, Info, TrendingUp } from 'lucide-react';

const SignalItem = ({ text, type }) => (
  <div className="flex items-start space-x-2">
    {type === 'positive' ? (
      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 mt-0.5 flex-shrink-0" />
    ) : (
      <XCircle className="w-3.5 h-3.5 text-red-400 mt-0.5 flex-shrink-0" />
    )}
    <span className="text-[11px] leading-relaxed text-gray-700 font-medium">{text}</span>
  </div>
);

const ShortlistPanel = ({ result }) => {
  const { shortlist_estimation } = result;
  const { 
    probability_label, 
    confidence, 
    disclaimer, 
    positive_signals, 
    negative_signals, 
    explanation 
  } = shortlist_estimation;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      {/* Hero Section */}
      <div className="bg-indigo-600 p-8 text-center text-white relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 -mr-8 -mt-8 w-32 h-32 bg-indigo-500/20 rounded-full blur-2xl" />
        <div className="absolute bottom-0 left-0 -ml-4 -mb-4 w-24 h-24 bg-white/10 rounded-full blur-xl" />
        
        <div className="relative z-10 space-y-2">
          <div className="flex items-center justify-center space-x-2 mb-1">
            <TrendingUp className="w-4 h-4 text-indigo-200" />
            <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-100">
              Estimated Shortlist Probability
            </span>
          </div>
          <h3 className="text-5xl font-black tracking-tight">{probability_label}</h3>
          <div className="pt-2">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-widest ${
              confidence === 'high' ? 'bg-emerald-400/20 text-emerald-100 border border-emerald-400/30' :
              confidence === 'medium' ? 'bg-yellow-400/20 text-yellow-100 border border-yellow-400/30' :
              'bg-amber-400/20 text-amber-100 border border-amber-400/30'
            }`}>
              {confidence} Confidence
            </span>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Explanation */}
        <div className="flex items-start space-x-3 bg-gray-50 p-4 rounded-xl border border-gray-100">
          <Info className="w-4 h-4 text-indigo-500 mt-0.5 flex-shrink-0" />
          <p className="text-xs text-gray-700 leading-relaxed font-medium">
            {explanation}
          </p>
        </div>

        {/* Signals Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest flex items-center">
              Positive Signals
              <span className="ml-1.5 w-1 h-1 bg-gray-300 rounded-full" />
            </h4>
            <div className="space-y-2">
              {positive_signals?.map((signal, idx) => (
                <SignalItem key={idx} text={signal} type="positive" />
              ))}
            </div>
          </div>
          
          <div className="space-y-3">
            <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest flex items-center">
              Negative Signals
              <span className="ml-1.5 w-1 h-1 bg-gray-300 rounded-full" />
            </h4>
            <div className="space-y-2">
              {negative_signals?.map((signal, idx) => (
                <SignalItem key={idx} text={signal} type="negative" />
              ))}
            </div>
          </div>
        </div>

        {/* Disclaimer - ALWAYS VISIBLE */}
        <div className="pt-4 border-t border-gray-100">
          <div className="flex items-start space-x-2">
            <Shield className="w-3.5 h-3.5 text-gray-400 mt-0.5 flex-shrink-0" />
            <p className="text-[10px] text-gray-400 leading-relaxed uppercase font-semibold tracking-tight">
              {disclaimer}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShortlistPanel;
