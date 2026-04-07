/**
 * Returns Tailwind color class string based on score
 * red(0-39), amber(40-59), yellow(60-74), green(75-89), emerald(90-100)
 */
export const getScoreColor = (score) => {
  if (score < 40) return 'text-red-500';
  if (score < 60) return 'text-amber-500';
  if (score < 75) return 'text-yellow-500';
  if (score < 90) return 'text-green-500';
  return 'text-emerald-500';
};

/**
 * Returns Tailwind bg class string based on score
 */
export const getScoreBgColor = (score) => {
  if (score < 40) return 'bg-red-500';
  if (score < 60) return 'bg-amber-500';
  if (score < 75) return 'bg-yellow-500';
  if (score < 90) return 'bg-green-500';
  return 'bg-emerald-500';
};

/**
 * Returns stroke color hex for SVG rings based on score
 */
export const getScoreRingColor = (score) => {
  if (score < 40) return '#ef4444'; // text-red-500
  if (score < 60) return '#f59e0b'; // text-amber-500
  if (score < 75) return '#eab308'; // text-yellow-500
  if (score < 90) return '#22c55e'; // text-green-500
  return '#10b981'; // text-emerald-500
};

/**
 * Returns label string based on score
 */
export const getScoreGrade = (score) => {
  if (score < 40) return 'Poor';
  if (score < 60) return 'Fair';
  if (score < 75) return 'Good';
  if (score < 90) return 'Strong';
  return 'Excellent';
};

/**
 * Maps high/medium/low/irrelevant to Tailwind classes
 */
export const getRelevanceBadgeColor = (relevance) => {
  switch (relevance?.toLowerCase()) {
    case 'high':
      return 'bg-emerald-100 text-emerald-700 border-emerald-200';
    case 'medium':
      return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    case 'low':
      return 'bg-amber-100 text-amber-700 border-amber-200';
    case 'irrelevant':
      return 'bg-red-100 text-red-700 border-red-200';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-200';
  }
};

/**
 * Maps high/medium/low to Tailwind classes
 */
export const getPriorityBadgeColor = (priority) => {
  switch (priority?.toLowerCase()) {
    case 'high':
      return 'bg-red-100 text-red-700 border-red-200';
    case 'medium':
      return 'bg-amber-100 text-amber-700 border-amber-200';
    case 'low':
      return 'bg-green-100 text-green-700 border-green-200';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-200';
  }
};

/**
 * Maps critical/moderate/minor to Tailwind classes
 */
export const getSeverityBadgeColor = (severity) => {
  switch (severity?.toLowerCase()) {
    case 'critical':
      return 'bg-red-100 text-red-700 border-red-200';
    case 'moderate':
      return 'bg-amber-100 text-amber-700 border-amber-200';
    case 'minor':
      return 'bg-gray-100 text-gray-700 border-gray-200';
    default:
      return 'bg-blue-100 text-blue-700 border-blue-200';
  }
};
